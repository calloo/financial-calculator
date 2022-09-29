from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


class ActionType(Enum):
    ADD = 'add'
    SUBTRACT = 'sub'
    SET = 'set'

    @staticmethod
    def value_from(name: str) -> Optional[ActionType]:
        return next(filter(
            lambda i: i.value == name,
            (i for i in ActionType)
        ))


class Sprite(Enum):
    BIRD = 'assets/bird.gif'
    CAKE = 'assets/cake.gif'
    ELEPHANT = 'assets/elephant.gif'
    FISH = 'assets/fish.gif'
    GAME = 'assets/game.gif'
    HEARTBEAT = 'assets/heartbeat.gif'
    PONY = 'assets/pony.gif'
    SHEEP = 'assets/sheep.gif'
    SNOW_FIGHT = 'assets/snow-fight.gif'
    STARWARS = 'assets/starwars.gif'
    NONE = ''


@dataclass
class Calculator:
    initial_deposit: float = 1000
    contribution_amount: float = 23230
    investment_timespan: int = 10
    estimated_return: float = 120
    future_balance: float = 0
    contribution_period: int = 1
    compound_period: int = 365
    sprite: Sprite = Sprite.STARWARS
    goal: float = 1000

    def get_sprite(self):
        return self.sprite.value

    def get_amount(self, field: str):
        """
        Used to retrieve values from the calculator. E.g. initial deposit
        :param field: name of the field
        :return:
        """
        return getattr(self, field)

    def change_amount(self, field: str, amount: float, action_string: str):
        """
        Used to change a property on the calculator. E.g. initial deposit, contribution amount e.t.c
        :param field:
        :param amount:
        :param action_string:
        :return:
        """
        action = ActionType.value_from(action_string)
        change = getattr(self, field)

        if action == ActionType.ADD:
            change += amount
        elif action == ActionType.SUBTRACT:
            change -= amount
        elif action == ActionType.SET:
            change = amount

        if change >= 0:
            setattr(self, field, change)
            return change
        return getattr(self, field)

    def calculate_future_values(self):
        """
        Calculates the future value
        """
        current_year = datetime.now().year
        labels = [year for year in range(current_year, current_year + int(self.investment_timespan))]
        principal_dataset = {
            "label": 'Total Principal',
            "backgroundColor": 'rgb(0, 123, 255)',
            "data": []
        }
        earnings_dataset = {
            "label": "Total Earnings",
            "backgroundColor": 'rgb(23, 162, 184)',
            "data": []
        }

        for time in range(1, self.investment_timespan + 1):
            principal = self.initial_deposit + (self.contribution_amount * self.contribution_period * time)
            earnings = 0
            balance = principal
            estimated_return = self.estimated_return / 100

            if estimated_return:
                gains = (1 + estimated_return / self.compound_period) ** (self.compound_period * time)
                compound_earnings = self.initial_deposit * gains
                contribution_earnings = self.contribution_amount * (gains - 1) / (estimated_return / self.contribution_period)
                earnings = compound_earnings + contribution_earnings - principal
                balance = compound_earnings + contribution_earnings

            self.future_balance = balance
            principal_dataset['data'].append(round(principal, 2))
            earnings_dataset['data'].append(round(earnings, 2))

        return {
            "labels": labels,
            "principal_dataset": principal_dataset,
            "earnings_dataset": earnings_dataset
        }
