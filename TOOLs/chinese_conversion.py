from opencc import OpenCC
# can also set conversion by calling set_conversion
# cc.set_conversion('s2tw')

def s2tw(to_convert):
    cc = OpenCC('s2tw') 
    converted = cc.convert(to_convert)
    return converted

def tw2s(to_convert):
    cc = OpenCC('tw2s')
    converted = cc.convert(to_convert)
    return converted

def s2twp(to_convert):
    cc = OpenCC('s2twp') 
    converted = cc.convert(to_convert)
    return converted

def tw2sp(to_convert):
    cc = OpenCC('tw2sp')
    converted = cc.convert(to_convert)
    return converted

if __name__ == "__main__":
    print(tw2s("開放中文轉換，馬鈴薯"))
    print(s2tw("开放中文转换，土豆"))

    # Phrase conversion is not working 
    print(tw2sp("開放中文轉換，馬鈴薯"))
    print(s2twp("开放中文转换，土豆"))