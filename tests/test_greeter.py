
from greeter.greeter import Greeter


def test_hello():
    obj = Greeter("myname")
    obs_str = obj.say_hello(time_of_day = "morning")
    exp_str = f"Good morning, myname!"

    assert obs_str == exp_str


def test_bye():
    obj = Greeter("myname")
    obs_str = obj.say_bye(friend = "fulana")
    exp_str = f"Bye, myname and fulana!"

    assert obs_str == exp_str
