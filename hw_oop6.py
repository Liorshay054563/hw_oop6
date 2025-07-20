# hw oop 6

from abc import ABC, abstractmethod

class ITransfer(ABC):
    @abstractmethod
    def transfer(self, amount: float, to_account) -> bool:
        pass

class IVerifyCreditCard(ABC):
    @abstractmethod
    def verify_credit_card(self, card_number: str) -> bool:
        pass

class IVerifyPayPal(ABC):
    @abstractmethod
    def verify_paypal_email(self, email: str) -> bool:
        pass


class BankAccount(ITransfer, IVerifyCreditCard, IVerifyPayPal):
    def __init__(self, id: str, balance: float, credit_card_number: str = None, paypal_email: str = None):
        self._id = id
        self._balance = balance
        self._credit_card_number = credit_card_number
        self._paypal_email = paypal_email

    def transfer(self, amount: float, to_account) -> bool:
        if self._balance >= amount:
            self._balance -= amount
            to_account._balance += amount
            return True
        return False

    def verify_credit_card(self, card_number) -> bool:
        return self._credit_card_number == card_number

    def verify_paypal_email(self, email) -> bool:
        return self._paypal_email == email

    @property # getter
    def balance(self):
        return self._balance


    @property # getter
    def id(self):
        return self._id

    def __str__(self):
        return (f"Account ID: {self._id}, Balance: {self._balance},\n"
                f" Credit Card: {self._credit_card_number}, PayPal: {self._paypal_email}")



class Payment(ABC):
    def __init__(self, amount: float, from_account_id: str, to_account_id: str):
        self.amount = amount
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id

    @abstractmethod
    def process(self, accounts) -> bool:
        pass

class CreditCardPayment(Payment):
    def __init__(self, amount: float, from_account_id: str, to_account_id: str, card_number: str):
        super().__init__(amount, from_account_id, to_account_id)
        self.card_number = card_number

    def process(self, accounts) -> bool:
        from_account = accounts[self.from_account_id]
        if from_account.verify_credit_card(self.card_number):
            if from_account.transfer(self.amount, accounts[self.to_account_id]):
                return True
        return False

class PayPalPayment(Payment):
    def __init__(self, amount: float, from_account_id: str, to_account_id: str, email: str):
        super().__init__(amount, from_account_id, to_account_id)
        self.email = email

    def process(self, accounts) -> bool:
        from_account = accounts[self.from_account_id]
        if from_account.verify_paypal_email(self.email):
            if from_account.transfer(self.amount, accounts[self.to_account_id]):
                return True
        return False


def main():
    accounts = {
        "A001": BankAccount("A001", 1000.0, credit_card_number="1234567890123456", paypal_email="user1@example.com"),
        "A002": BankAccount("A002", 500.0, credit_card_number="1111222233334444", paypal_email="user2@example.com")
    }

    payments = [
        CreditCardPayment(200.0, "A001", "A002", card_number="1234567890123456"),  # valid
        PayPalPayment(300.0, "A001", "A002", email="wrong@example.com"),           # invalid email
        CreditCardPayment(900.0, "A002", "A001", card_number="1111222233334444")   # insufficient funds
    ]

    for payment in payments:
        print(payment.process(accounts))
        print("-" * 40)

    for acc in accounts.values():
        print(acc)

# main
if __name__ == "__main__":
    main()