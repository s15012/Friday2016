
#画面に自分の学科名　学年　学籍番号を出力してください
def print_self_information():
    print("ITspecialist \n Grade:2 \n S15012")




#自分の年齢が、80歳になるまで後何年か計算してください
def print_how_many_years_to_80():
    myAge = 20
    futureAge = 80
    how_many_years = futureAge - myAge

    print("あなたが80歳になるまで後", how_many_years, "年です。")



#与えられたパラメータが偶数　か　奇数　かを出力してください
def print_odd_or_even(target):

    if (target % 2 == 0):
        print("偶数")
    else:
        print("奇数")


#randomモジュールを使用して0−50の整数を生成し、25が出るまで　ほげ　と出力してください
def print_hoge():
    from random import randint

    while(True):
        hoge = randint(0,50)
        if (hoge == 25):
            print(hoge,"が出ました！")
            break;
        else:
            print("ほげほげ\n")






#100から1000までの偶数のみ表示してください
def print_even_from_100_to_1000():
    for i in range(100,1000):
        if (i % 2 == 0):
            print(i)
        else:
            pass



if __name__ == '__main__':

    print_self_information()
    print_how_many_years_to_80()
    print_odd_or_even(10)
    print_odd_or_even(13)
    print_hoge()
    print_even_from_100_to_1000()