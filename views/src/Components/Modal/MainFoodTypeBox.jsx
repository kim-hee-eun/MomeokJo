import React from 'react';
import FoodImgModal from './FoodImgModal';
// 이미지 경로 정의
import img1 from '../../Image/곡류및서류.jpg';
import img2 from '../../Image/과자류.jpg';
import img3 from '../../Image/구이류.jpg';
import img4 from '../../Image/국및탕류.jpg';
import img5 from '../../Image/기타.jpg';
import img6 from '../../Image/김치류.jpg';
import img7 from '../../Image/면및만두류.jpg';
import img8 from '../../Image/밥류.jpg';
import img9 from '../../Image/볶음류.jpg';
import img10 from '../../Image/빵류.jpg';
import img11 from '../../Image/생채및무침류.jpg';
import img12 from '../../Image/숙채류.jpg';
import img13 from '../../Image/아이스크림류.jpg';
import img14 from '../../Image/음료및차류.jpg';
import img15 from '../../Image/전,적및부침류.jpg';
import img16 from '../../Image/조림류.jpg';
import img17 from '../../Image/죽및스프류.jpg';
import img18 from '../../Image/찌개및전골류.jpg';
import img19 from '../../Image/찜류.jpg';
import img20 from '../../Image/튀김류.jpg';
import img21 from '../../Image/회류.jpg';

export default function MainFoodTypeBox({
  recommendedFood,
  selectFoodHandler,
}) {
  // mainFoodType에 따라 이미지 선택
  let mainFoodTypeImage;
  switch (recommendedFood.mainFoodType) {
    case '곡류 및 서류':
      mainFoodTypeImage = img1;
      break;
    case '과자류':
      mainFoodTypeImage = img2;
      break;
    case '구이류':
      mainFoodTypeImage = img3;
      break;
    case '국 및 탕류':
      mainFoodTypeImage = img4;
      break;
    case '기타':
      mainFoodTypeImage = img5;
      break;
    case '김치류':
      mainFoodTypeImage = img6;
      break;
    case '면 및 만두류':
      mainFoodTypeImage = img7;
      break;
    case '밥류':
      mainFoodTypeImage = img8;
      break;
    case '볶음류':
      mainFoodTypeImage = img9;
      break;
    case '빵류':
      mainFoodTypeImage = img10;
      break;
    case '생채 및 무침류':
      mainFoodTypeImage = img11;
      break;
    case '숙채류':
      mainFoodTypeImage = img12;
      break;
    case '아이스크림류':
      mainFoodTypeImage = img13;
      break;
    case '음료 및 차류':
      mainFoodTypeImage = img14;
      break;
    case '전적 및 부침류':
      mainFoodTypeImage = img15;
      break;
    case '조림류':
      mainFoodTypeImage = img16;
      break;
    case '죽 및 스프류':
      mainFoodTypeImage = img17;
      break;
    case '찌개 및 전골류':
      mainFoodTypeImage = img18;
      break;
    case '찜류':
      mainFoodTypeImage = img19;
      break;
    case '튀김류':
      mainFoodTypeImage = img20;
      break;
    case '회류':
      mainFoodTypeImage = img21;
      break;
    default:
      mainFoodTypeImage = ''; 
  }
  console.log(mainFoodTypeImage);
  return (
    <div
      className="mainFoodType-box"
      style={{
        backgroundImage: `url(${mainFoodTypeImage})`,
      }}
      onClick={() => selectFoodHandler(recommendedFood)}
    >
      <FoodImgModal recommendedFood={recommendedFood} />
    </div>
  );
}