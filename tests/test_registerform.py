from spork.models.registerform import RegisterForm
import pytest


def test_constructor():
    rf=RegisterForm("test@test.com","AAa2341@13w","AAa2341@13w")
    assert rf.email == "test@test.com"
    assert rf.password == "AAa2341@13w"
    assert rf.confirm_password == "AAa2341@13w"

def test_check_confirm_password_success():
    rf=RegisterForm("test@test.com","AAa2341@13w","AAa2341@13w")
    assert rf.check_confirm_password() == True

    rf=RegisterForm("test@test.com","","")
    assert rf.check_confirm_password() == True

def test_check_confirm_password_failure():
    rf=RegisterForm("test@test.com","aaa2341@13w","AAa2341@13w")
    assert rf.check_confirm_password() == False

    rf=RegisterForm("test@test.com","1","11")
    assert rf.check_confirm_password() == False

def test_check_email_success():
    rf=RegisterForm("test@test.com","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == True
    rf=RegisterForm("test@t.co","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == True
    rf=RegisterForm("a@test.com.hk","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == True
    rf=RegisterForm("test@test-example.com","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == True
    rf=RegisterForm("adni.sad@gmail.com","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == True

def test_check_email_faiilure():
    rf=RegisterForm(1,"AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == False
    rf=RegisterForm("a@j233","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == False
    rf=RegisterForm("asdas@test.c.ca","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == False
    rf=RegisterForm("asdas@test3!.ca.ca","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == False
    rf=RegisterForm("t@.co","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == False
    rf=RegisterForm("@","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == False
    rf=RegisterForm("","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == False
    rf=RegisterForm("aa@ssd@sd.com","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == False
    rf=RegisterForm("abc@sbd_asd.com","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == False
    rf=RegisterForm("abc!sk@gmail.com","AAa2341@13w","AAa2341@13w")
    assert rf.check_email() == False

def test_check_password_strength_success():
    rf=RegisterForm("test@test.com","AAa2341@13w","AAa2341@13w")
    assert rf.check_password_strength() == True
    rf=RegisterForm("test@test.com","a23A4113w!","a23A4113w!")
    assert rf.check_password_strength() == True


def test_check_password_strength_failure():
    rf=RegisterForm("test@test.com","1234567","1234567")
    assert rf.check_password_strength() == False
    rf=RegisterForm("test@test.com","A1234567","A1234567")
    assert rf.check_password_strength() == False
    rf=RegisterForm("test@test.com","Aa1234567","Aa1234567")
    assert rf.check_password_strength() == False
    rf=RegisterForm("test@test.com","Aa123!","Aa123")
    assert rf.check_password_strength() == False
    rf=RegisterForm("test@test.com","AAAAAAAAAAAaa@@","AAAAAAAAAAAaa@@")
    assert rf.check_password_strength() == False
