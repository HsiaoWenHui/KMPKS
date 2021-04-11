# KM=(P+K)^S
利用網站系統以文章形式將成員知識外化後分享交流，使知識匯集後能夠增加學習效果
===========================================================================
命名規則 ref:https://medium.com/mr-efacani-teatime/%E6%92%B0%E5%AF%AB%E7%A8%8B%E5%BC%8F%E7%9A%84%E7%AC%AC%E4%B8%80%E6%AD%A5-%E5%AD%B8%E7%BF%92%E6%9C%89%E6%84%8F%E7%BE%A9%E7%9A%84%E5%91%BD%E5%90%8D-62252ea86587

【變數或函數】少用縮寫，多使用完整單字，單字間用下劃線『 _ 』區隔
int file_age_in_days; // 變數使用小寫
int STATUS_VALUE; //常數使用大寫
class Member(){
    private int _memeber_id; //類別內的私用成員變數，以下劃線開頭
    set_member_id(int member_id){
        _member_id=member_id; //更容易區別參數與私用變數
    }
}

【類別或文件】採用名詞命名，使用駝峰式命名法，若有縮寫則用下劃線『 _ 』區隔
class UserRecord(){...}
class WebPagePrinter(){...}
class HTML_Parser(){...} //遇到縮寫用下劃線『 _ 』區隔


【命名空間】基於專案名稱或目錄結構
namespace www.example.com/api/SystemMembers 用小寫命名, 並基於專案名稱和目錄結構:www/example/com/api/SystemMembers.js


函數方法採用動詞開頭
採用動詞開頭，且避免語意不清
// REST Style
get 取值：
get_member(id) //取得編號id的會員
delete 刪除：
delete_member(id) //刪除編號id的會員
put 搬移或替換：
put_member(member_object,id) //將member_object搬移至編號id的這個位置，如果id不存在就建立一個新的member
patch 部分更新：
patch_member(memeber_data_list,id) //根據member_data_list提供的內容去更新編號id的會員
post 建立：
post_member(member_data_list)  //根據member_data_list建立一個新會員
//其他常見動詞
is 狀態判斷：
isMember(account_name) //判斷account_name是否是會員
save 儲存
copy 複製
append 附加

命名的長度應該與其視野(scope)的大小相對應
//變數i的調用範圍只在單一迴圈內，所以使用單一字母的變數也不會影響可讀性
for(int i;i<10;i++){
    //do something
}
int WORK_DAYS_PER_WEEK=5 //調用範圍越大的變數，盡量使其容易被搜尋，長命名勝過短命名