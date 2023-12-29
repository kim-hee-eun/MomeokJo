const express = require('express');
const morgan = require('morgan');
const path = require('path');
const dotenv = require('dotenv');
const xlsx = require('xlsx');
const FoodItem = require('./models/fooditem');
const cors = require('cors');

dotenv.config();

const userRouter = require('./routes/user');
const recommendRouter = require('./routes/recommend');
const selectrecordRouter = require('./routes/selectrecord');
const { sequelize } = require('./models');

const app = express();
//passportConfig(); // 패스포트 설정
app.set('port', process.env.PORT || 60024);
app.set('hostname', );

const connectDatabaseAndImportData = async () => {
  try {
    console.log('데이터베이스 연결 중...');
    await sequelize.sync({ force: false }); // 테이블 초기화
    console.log('데이터베이스 연결 성공');

    const workbook = xlsx.readFile('./public/food_db_result_final.xlsx');
    const worksheet = workbook.Sheets[workbook.SheetNames[0]];
    const excelDataArray = xlsx.utils.sheet_to_json(worksheet, { header: 1 });
    //excelDataArray.length
    for (let rowIndex = 1; rowIndex < excelDataArray.length; rowIndex++) {
      const [
        code,
        name,
        mainFoodType,
        detailedFoodType,
        servingSize,
        calorie,
        protein,
        fat,
        carbohydrate,
        sugar,
        sodium,
        cholesterol,
        saturatedFattyAcid,
        transFattyAcid,
        taste,
        mainIngredient,
        secondaryIngredient,
        cookMethod,
        allergens
      ] = excelDataArray[rowIndex];

      // 데이터베이스에 이미 존재하는지 확인
      if (code === undefined) {
        continue;
      }
      const existingData = await FoodItem.findOne({ where: { code } });
      if (!existingData) {
        // 존재하지 않으면 저장
        await FoodItem.create({
          code,
          name,
          mainFoodType,
          detailedFoodType,
          servingSize,
          calorie,
          protein,
          fat,
          carbohydrate,
          sugar,
          sodium,
          cholesterol,
          saturatedFattyAcid,
          transFattyAcid,
          taste,
          mainIngredient,
          secondaryIngredient,
          cookMethod,
          allergens
        });
      }
    }
    
    console.log('데이터베이스에 저장 완료');
  } catch (error) {
    console.error('데이터베이스 연결 또는 저장 중 오류 발생:', error);
  }
};
connectDatabaseAndImportData();

app.get('/mypage', (req, res) => { res.sendFile(path.join(__dirname + '/views/build/index.html')); });
app.get('/foodrecommend', (req, res) => { res.sendFile(path.join(__dirname + '/views/build/index.html')); });
app.get('/aboutus', (req, res) => { res.sendFile(path.join(__dirname + '/views/build/index.html')); });
app.get('/login', (req, res) => { res.sendFile(path.join(__dirname + '/views/build/index.html')); });
app.get('/join', (req, res) => { res.sendFile(path.join(__dirname + '/views/build/index.html')); });
app.get('/editpersonalinfo', (req, res) => { res.sendFile(path.join(__dirname + '/views/build/index.html')); });
app.get('/', (req, res) => { res.sendFile(path.join(__dirname + '/views/build/index.html')); });

// 모든 경로에 대해 CORS 허용
app.use(cors());
app.use(morgan('dev'));
app.use(express.static(path.join(__dirname, 'views/build')));
app.use(express.json());

app.use('/user', userRouter);
app.use('/foodRecommend', recommendRouter);
app.use('/selectrecord', selectrecordRouter);

app.use((req, res, next) => {
  const error =  new Error(`${req.method} ${req.url} 라우터가 없습니다.`);
  error.status = 404;
  next(error);
});

app.use((err, req, res, next) => {
  res.locals.message = err.message;
  res.locals.error = process.env.NODE_ENV !== 'production' ? err : {};
  res.status(err.status || 500).json({
    message: err.message,
    error: process.env.NODE_ENV !== 'production' ? err : {},
  });
});

app.listen(app.get('port'), () => {
  console.log(app.get('port'), '번 포트에서 대기중');

});
