This is wzk's personal python library~



# How to install?
simply run `pip install wzk`. That's it!





# What can you do?


## Entertainment

### play games
Each with an interesting console game
```python
import wzk
wzk.flight_game()
wzk.game2048()
wzk.mine_sweep()
wzk.texas_poker()
wzk.pokemon()
wzk.mahjong()
```



## Academic 

### look up english words in dictionary

Off-line Chinese-English dictionary with more than 100k words
```python
import wzk
wzk.lookup("good", verbose=True, non_alpha=False")
wzk.translate("I love you"):
```

### check your OO homework

Generate data, judge your results, and beatmatch with peers

Note: made in 2020, may not be applicable in later years

```python
from wzk.oo2020 import *

beatmatch(["test1.txt","test2.txt","test3.txt"])
print(hw3_generator(10))
print(hw7_generator(10,3,10))
print(hw11_generator(10,5))
print(hw13_generator())
print(derivative_judge("3*x**2","x**3"))
print(hw5_judge(open("out.txt").read(), open("data.txt").read()))
```

### NLP metric

Calculate BLEU score

```python
from wzk.nlp import bleu
print(bleu("they are good", "they are not good", k=2))
```



## Useful Tools

### send email

Send email with SMTP
```python
import wzk
sender = wzk.parser.MailSender(mail_host, mail_user, mail_pass)
sender.send_mail(title="hi~", content="nothing~", receiver=None)
```

### check web page update
Automatically check web page and send notification email when update
```python
import wzk
checker = wzk.parser.WebPageUpdateChecker(mail_host, mail_user, mail_pass)
checker.check("www.baidu.com", interval=10)
```



## For Developers

### improved data structure

Dictionary supporting inverse-mapping and attribute-indexing

Number type supporting setting bound and loop

```python
from wzk import DD, N

a = DD({"good": "kk"})
a.bad = "nyima"
print(a.good)
print(a["bad"])
print(a.inv())
print(a.inv().inv())

b = N(4, upper_bound=8, lower_bound=3)
b += 5
c = N(4, upper_bound=8, lower_bound=3, loop=True)
print(c+5)
```
### interestring utensils

Several interesing utensils

```python
import time
from wzk import ErrorFucker, Separate, Clock

with ErrorFucker(raises=False) as ef1:
    d1 = int("f")

with Separate("separate zone", count=True) as s:
    print("ohhh")

with s:
    with Clock("test") as c:
        time.sleep(2)
    print(c)

with ErrorFucker(raises=True) as ef2:
    d2 = int("d")
```

### simplified pytorch(?)

Scalar autograd mechanism

```python
from wzk.autograd.thing import *

a = thing(2)
b = thing(3)
c = a + leaky_relu(b)
d = thing(5) # a + a*b
e = tanh(d) # (a + a*b) * (a*b) = a^2(b + b^2)
f = relu(c) + sin(e)
g = log(f)

g.backward()
print(a)
print(b)
print(c)
print(d)
print(e)
print(f)
print(g)
```

