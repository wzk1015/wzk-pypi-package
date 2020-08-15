This is wzk's personal python library~



## How to install?
simply run `pip install wzk`. That's it!



## What can you do?
First, `import wzk`

### play games
Each with an interesting console game!
```python
wzk.flight_game()
wzk.game2048()
wzk.mine_sweep()
wzk.texas_poker()
wzk.pokemon()
wzk.mahjong()
```

### look up english words in dictionary
Off-line Chinese-English dictionary with more than 100k words!
```python
wzk.lookup("good", verbose=True, non_alpha=False")
wzk.translate("I love you"):
```


### send email
Send email with SMTP!
```python
sender = wzk.parser.MailSender(mail_host, mail_user, mail_pass)
sender.send_mail(title="hi~", content="nothing~", receiver=None)
```

### check web page update
Automatically check web page and send notification email when update!
```python
checker = wzk.parser.WebPageUpdateChecker(mail_host, mail_user, mail_pass)
checker.check("www.baidu.com", interval=10)
```

### use improved data structure
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
Dictionary supporting inverse-mapping and attribute-indexing！

Number type supporting setting bound and loop!

