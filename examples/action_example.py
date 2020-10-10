#!/usr/bin/env python

from commlib.transports.redis import (ActionServer, ActionClient,
                                      ConnectionParameters)
from commlib.action import GoalStatus
from commlib.msg import ActionMessage, DataClass
import time


class ExampleAction(ActionMessage):
    @DataClass
    class Goal(ActionMessage.Goal):
        target_cm: int = 0

    @DataClass
    class Result(ActionMessage.Result):
        dest_cm: int = 0

    @DataClass
    class Feedback(ActionMessage.Feedback):
        current_cm: int = 0


def on_goal(goal_h, result_msg, feedback_msg):
    c = 0
    while c < 5:
        goal_h.send_feedback(feedback_msg(current_cm=c))
        c += 1
        time.sleep(1)
    res = result_msg(dest_cm=c)
    return res

def on_feedback(feedback):
    print(feedback)


def on_result(result):
    print(result)


if __name__ == '__main__':
    action_name = 'testaction'
    conn_params = ConnectionParameters()
    action = ActionServer(msg_type=ExampleAction,
                          conn_params=conn_params,
                          action_name=action_name,
                          on_goal=on_goal)
    action_c = ActionClient(msg_type=ExampleAction,
                            conn_params=conn_params,
                            action_name=action_name,
                            on_feedback=on_feedback,
                            on_result=on_result)

    action.run()
    time.sleep(1)

    goal_msg = ExampleAction.Goal()

    action_c.send_goal(goal_msg)
    res = action_c.get_result(wait=True)
    print(res)
    while True:
        time.sleep(0.01)
