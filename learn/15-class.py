# 类定义
class people:
  # 定义基本属性
  name = ''
  age = 0
  # 定义私有属性,私有属性在类外部无法直接进行访问
  __weight = 0
  # 定义构造方法

  def __init__(self, n, a, w):
    self.name = n
    self.age = a
    self.__weight = w

  def speak(self):
    print("%s 说: 我 %d 岁。" % (self.name, self.age))


# 实例化类
p = people('runoob', 10, 30)
p.speak()


class A:
  aa = 10

  def __init__(self, a, b):
    self.a = a
    self.b = b


a = A(5, 20)

print(A.aa)
print(a.a)  # 实例变量
print((a.aa))  # 实例读取类变量

# 类定义


class people:
  # 定义基本属性
  name = ''
  age = 0
  # 定义私有属性,私有属性在类外部无法直接进行访问
  __weight = 0
  # 定义构造方法

  def __init__(self, n, a, w):
    self.name = n
    self.age = a
    self.__weight = w

  def speak(self):
    print("%s 说: 我 %d 岁。" % (self.name, self.age))

# 单继承示例


class student(people):
  grade = ''

  def __init__(self, n, a, w, g):
    # 调用父类的构函
    people.__init__(self, n, a, w)
    self.grade = g
  # 覆写父类的方法

  def speak(self):
    print("%s 说: 我 %d 岁了，我在读 %d 年级" % (self.name, self.age, self.grade))


s = student('ken', 10, 60, 3)
s.speak()


class Parent:        # 定义父类
  def myMethod(self):
    print('调用父类方法')


class Child(Parent):  # 定义子类
  def myMethod(self):
    super(Child, self).myMethod()
    print('调用子类方法')


c = Child()          # 子类实例
c.myMethod()         # 子类调用重写方法
super(Child, c).myMethod()  # 用子类对象调用父类已被覆盖的方法
