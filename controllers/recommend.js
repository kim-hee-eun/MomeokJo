const { spawnSync } = require('child_process');
const { Op } = require('sequelize');
const path = require('path');

const User = require('../models/user');
const FoodItem = require('../models/fooditem');

// Python 스크립트 실행 함수
const runPythonScript = (scriptPath, ...args) => {
  try {
    const result = spawnSync('python', [scriptPath, ...args], {
      env: {
        ...process.env,
        PYTHONIOENCODING: 'utf-8',
      },
    });  
 
    if (result.error) {
      throw new Error(`Error running Python script: ${result.error}`);
    }
    const outputData = JSON.parse(result.stdout.toString());
    const errorData = result.stderr.toString();
    if (errorData) {
      throw new Error(`Python script error: ${errorData}`);
    }

    return outputData;
  } catch (error) {
    console.error(error.message);
    return null;
  }
};

// 사용자 정보로 ERR 계산 함수
const getUserERR = (userInfo) => runPythonScript('./controllers/ERR.py', JSON.stringify(userInfo));

// 일일 섭취 식품 정보 얻기 함수
const getUserDailyfood = dailyfood => runPythonScript('./controllers/UserFoodMatchAndInfo.py', dailyfood);

// 사용자의 음식 추천 함수
const getUserRecommendFood = (userPreference, nutrientRecommendedFoods) => {
  const jsonString1 = JSON.stringify(userPreference);
  
  const foodNamesString = nutrientRecommendedFoods.map(food => food.name).join(',');
  const outputData = runPythonScript('./controllers/CatBoost_training_recommend.py', jsonString1, foodNamesString);

  if (outputData) {
    return outputData;
  }

  return null;
};

// 사용자 추천 및 영양 정보 가져오기 함수
exports.recommendation = async (req, res, next) => {
  try {
    let { dailyFood } = req.body;
    const user = await User.findOne({ where: { userId: res.locals.decoded.userId } });

    if (user) {
      const userInfo = {
        gender: user.gender,
        age: user.age,
        weight: user.weight,
        height: user.height,
        activityLevel: user.activityLevel
      };

      
      const userERR = await getUserERR(userInfo);
      
      const userNeedNutrient = {
        calorie: userERR.calorie,
        protein: userERR.protein_max,
        fat: userERR.fat_max,
        carbohydrate: userERR.carbohydrate_max,
      };

      const userNutrientRequirement = {
        calorie: userERR.calorie,
        protein: userERR.protein_max,
        fat: userERR.fat_max,
        carbohydrate: userERR.carbohydrate_max,
        sugar: userERR.sugar,
        sodium: userERR.sodium,
        cholesterol: userERR.cholesterol,
        saturatedFattyAcid: userERR.saturatedFattyAcid,
        transFattyAcid: userERR.transFattyAcid,
      };

      let userDailyfoods = null;
      let dailyFoodInfo = null;

      if (dailyFood !== "") {
        userDailyfoods = getUserDailyfood(dailyFood);
        
        if (userDailyfoods.data) {
          const namesArray = userDailyfoods.data;
          const nameStr = namesArray.join(',');

          const dailyFoodArray = dailyFood.split(',');
          dailyFoodInfo = [];

          let FoodNutrient = await FoodItem.findAll({
            where: { name: namesArray },
            attributes: [
              'name',
              'servingSize',
              'calorie',
              'protein',
              'fat',
              'carbohydrate',
              'sugar',
              'sodium',
              'cholesterol',
              'saturatedFattyAcid',
              'transFattyAcid',
            ],
            raw : true,
          });

          if (namesArray.length !== dailyFoodArray.length) {
            FoodNutrient.forEach((food, index) => {
              dailyFoodInfo.push({
                name: namesArray[index],
                servingSize: food.servingSize,
                calorie: food.calorie,
                protein: food.protein,
                fat: food.fat,
                carbohydrate: food.carbohydrate,
                sugar: food.sugar,
                sodium: food.sodium,
                cholesterol: food.cholesterol,
                saturatedFattyAcid: food.saturatedFattyAcid,
                transFattyAcid: food.transFattyAcid,
              });
              food.name = namesArray[index];
            });
          } else {
            FoodNutrient.forEach((food, index) => {
              dailyFoodInfo.push({
                name: dailyFoodArray[index],
                servingSize: food.servingSize,
                calorie: food.calorie,
                protein: food.protein,
                fat: food.fat,
                carbohydrate: food.carbohydrate,
                sugar: food.sugar,
                sodium: food.sodium,
                cholesterol: food.cholesterol,
                saturatedFattyAcid: food.saturatedFattyAcid,
                transFattyAcid: food.transFattyAcid,
              });
              food.name = dailyFoodArray[index];
            });
          }
        
          Object.keys(userNeedNutrient).forEach(key => {
              userNeedNutrient[key] -= dailyFoodInfo.reduce((acc, food) => acc + food[key], 0);
            });
        }
      }
      
      const userPreference = {
        spicyPreference: user.spicinessPreference,
        meatConsumption: user.meatConsumption,
        tastePreference: user.flavorPreference,
        activityLevel: user.activityLevel,
        preferenceTypeFood: user.foodTypePreference
      };

      const nutrientRecommendedFoods = await FoodItem.findAll({
        where: { 
          calorie: { [Op.lt]: userNeedNutrient.calorie },
          //protein: { [Op.lt]: userNeedNutrient.protein },
          //fat: { [Op.lt]: userNeedNutrient.fat },
          //carbohydrate: { [Op.lt]: userNeedNutrient.carbohydrate },
        },
        attributes: [
          'name',
        ],
        raw : true,
      });

      const lackNutrientInfo = [{
        name: "분석",
        calorie: userERR.calorie,
        protein: `${userERR.carbohydrate_min} ~ ${userERR.carbohydrate_max}`,
        fat: `${userERR.fat_min} ~ ${userERR.fat_max}`,
        carbohydrate: `${userERR.protein_min} ~ ${userERR.protein_max}`,
      }, {
        name: "평가",
        calorie: userNeedNutrient.calorie < 0 ? "포화" : "부족",
        protein: userNeedNutrient.protein < 0 ? "만족" : "부족",
        fat: userNeedNutrient.fat < 0 ? "만족" : "부족",
        carbohydrate: userNeedNutrient.carbohydrate < 0 ? "만족" : "부족",
      }];
      const userRecommendFood = getUserRecommendFood(userPreference, nutrientRecommendedFoods);

      if(userRecommendFood === null && userRecommendFood.length === 0){
        return res.status(200).json({
          lackNutrientInfo,
          dailyFoodInfo,
          userNutrientRequirement,
          recommendedFoods: null,
        });
      }

      const foodNames = userRecommendFood.map(food => food.name);

      const foods = await FoodItem.findAll({
        where: { name: foodNames },
        attributes: [
          'name',
          'calorie',
          'protein',
          'fat',
          'carbohydrate',
          'sugar',
          'sodium',
          'cholesterol',
          'saturatedFattyAcid',
          'transFattyAcid',
          'mainFoodType',
        ],
      });

    
      const recommendFood = [];
      const groupedByMainFoodType = {};
      
      foods.forEach(foodItem => {
        const mainFoodType = foodItem.dataValues.mainFoodType;

        if (!groupedByMainFoodType[mainFoodType]) {
          // 새로운 mainFoodType이 등장한 경우
          groupedByMainFoodType[mainFoodType] = {
            mainFoodTypeImg: `${mainFoodType}.jpg`,
            mainFoodType: mainFoodType,
            content: [],
          };
          recommendFood.push(groupedByMainFoodType[mainFoodType]);
        }

        // content에 해당 정보 추가
        groupedByMainFoodType[mainFoodType].content.push({
          name: foodItem.dataValues.name,
          calorie: foodItem.dataValues.calorie,
          protein: foodItem.dataValues.protein,
          fat: foodItem.dataValues.fat,
          carbohydrate: foodItem.dataValues.carbohydrate,
          sugar: foodItem.dataValues.sugar,
          sodium: foodItem.dataValues.sodium,
          cholesterol: foodItem.dataValues.cholesterol,
          saturatedFattyAcid: foodItem.dataValues.saturatedFattyAcid,
          transFattyAcid: foodItem.dataValues.transFattyAcid,
        });
      });

      return res.status(200).json({
        lackNutrientInfo,
        dailyFoodInfo,
        userNutrientRequirement,
        recommendedFoods: recommendFood
      }); //임시
    } else {
      return res.status(400).json({ success: false });
    }

  } catch (error) {
    console.error(error);
    next(error);
  }
};
  