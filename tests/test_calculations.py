import pytest 
from app.calculations import add, substract, multiply, divide
from app.calculations import BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)



@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected

def test_substract():
    assert substract(9, 4) == 5

def test_multiply():
    assert multiply(4, 3) == 12

def test_divide():
    assert divide(20, 5) == 4



def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_deposit(bank_account): 
    bank_account.deposit(20000)
    assert bank_account.balance == 20050

def test_withdraw(bank_account):
    bank_account.withdraw(50)
    assert bank_account.balance == 0

def test_collect_interest(bank_account):    
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55


@pytest.mark.parametrize("deposited, withdraw, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
])
def test_bank_transcations(zero_bank_account, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

def test_sufficient_funds(bank_account):
    # with pytest.raises(Exception):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)