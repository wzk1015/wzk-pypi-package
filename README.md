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

### use improved data structure

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
### discover interestring utensils

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

### use simplified pytorch(?)

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

