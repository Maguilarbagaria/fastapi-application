import pytest
from OwnProjects.APIproject.tests.calculations import add, substract, multiply, BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5),
    (10,5,15),
    (620,15,635)
])
def test_add(num1, num2, expected):
    print("Testing add function")

    assert add(num1, num2) == expected


def test_substract():
    print("susbtract test")

    assert substract(8,3) == 5

def test_multiply():
    print("multiply test")

    assert multiply(8,3) == 24


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):

    assert zero_bank_account.balance == 0

def test_bank_withdraw(bank_account):
    bank_account.withdraw(30)
    assert bank_account.balance == 20

def test_bank_diposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert int(bank_account.balance) == 55


@pytest.mark.parametrize("deposited, withdraw, expected", [
    (30,20,10),
    (1000,500,500),
    (72,2,70),
])
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert int(zero_bank_account.balance) == expected


def test_insufficient_funds(zero_bank_account):
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(50)

