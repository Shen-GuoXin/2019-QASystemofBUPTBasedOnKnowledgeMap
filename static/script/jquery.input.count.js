// JavaScript Document
// 限制输入字数
$(function () {
    var $tex = $(".faq-input-content .input");
    var $but = $(".faq-input-content .btn");
    var ie = jQuery.support.htmlSerialize;
    var str = 0;
    var abcnum = 0;
    var maxNum = 200;
    var texts = 0;
    var num = 0;
    var sets = null;

    $tex.val("");

    //提示文字
    $tex.focus(function () {
        if ($tex.val() == "") {
            $(".input-count").html("您还可以输入<span>100</span>个字");
        }
    })
    $tex.blur(function () {
        if ($tex.val() == "") {
            $(".input-count").html("");
        }
    })

    //文本框字数计算和提示改变
    if (ie) {
        $tex[0].oninput = changeNum;
    } else {
        $tex[0].onpropertychange = changeNum;
    }

    function changeNum() {
        //汉字的个数
        str = ($tex.val().replace(/\w/g, "")).length;
        //非汉字的个数
        abcnum = $tex.val().length - str;

        total = str * 2 + abcnum;

        if (str * 2 + abcnum < maxNum || str * 2 + abcnum == maxNum) {
            $but.removeClass();
            $but.addClass("btn");
            $but.attr("disabled", false);
            texts = Math.ceil((maxNum - (str * 2 + abcnum)) / 2);
            $(".input-count").html("您还可以输入<span>" + texts + "</span>个字").children().css({ "color": "#45a6a7" });
        } else if (str * 2 + abcnum > maxNum) {
            $but.removeClass();
            $but.addClass("btn2");
            $but.attr("disabled", true);
            texts = Math.ceil(((str * 2 + abcnum) - maxNum) / 2);
            $(".input-count").html("您输入的字数超过<span>" + texts + "</span>个了").children("span").css({ "color": "#e65b5b" });
        }
    }
})