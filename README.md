# k8-data-visualization

These are the coding guidelines we tend to follow for Python projects at Glasswall

- [Code Formatting](#code-format)
- [Naming Conventions](#naming-conventions)
- [General](#general)

<a id="code-format"></a>
## Code Formatting

* Align formatting of code using common sense

* Parameter formatting (Readable and easy to find issues if any)

<br><img src="./img/code_formatting.png" alt="Example Formatting" width="650"/><br>

* Code lengths should be based on code readability (for example in the case below)

```
	CONST PARTNERED = 'We have partenered with multiple clients to look out '\
    
                       'for opportunities to get more clientelle'
```

 It is better to put all of that in one line

```
	CONST PARTNERED = 'We have partenered with multiple clients to look out for opportunities to get more clientelle'
```


<a id="naming-conventions"></a>
## Naming Conventions

* Keep separate classes in separate files

* Class names to follow upper camel case (class names should have underscores between words)
e.g
```
	class Http_Api_Issues:
```

* File names should match the class name. E.g. Above file to be saved as “Http_Api_Issues.py”

* Function names to follow lower camel case e.g

e.g.
```
def get_all_issues():
```

* We don’t follow any standards e.g. PEP. Code readability and easy to understand and debug are must.

E.g. Compare a more readable code

```
CONST_STACKOVERFLOW            = 'stackoverflow'
CONST_GLASSWALL                = 'glasswall'
CONST_GW_PROXY                 = 'gw-proxy'
```

With a lesser readable one

```
CONST_STACKOVERFLOW='stackoverflow'
CONST_GLASSWALL='glasswall'
CONST_GW_PROXY='gw-proxy'
```

* Put CONST (when used) on separate python, json or yaml files


![Constants](./img/consts.png)



<a id="general"></a>
## General

* Commit often and with clear commit messages

* You can use whatever font size or face you want, as long as that setting is not pushed to the main repo 

* Align formatting of code using common sense
