const express = require('express');
const { verifyToken } = require('../middlewares');
const { join, login, userName, info, updateUserInfo } = require('../controllers/user');

const router = express.Router();

// POST /user
//회원가입 /user/join
router.post('/join', join); 

//로그인
router.post('/login', login);

//이름만
router.get('/name', verifyToken, userName);

//유저정보
router.get('/info', verifyToken, info);

//유저 정보 수정
router.post('/update', verifyToken, updateUserInfo);


module.exports = router;
