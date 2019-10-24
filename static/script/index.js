// JavaScript Document
$(document).ready(function () {
    $(".globe-naver li").hover(function () {
        $(this).addClass("selected");
    }, function () {
        $(this).removeClass("selected");
    });
});

// �����ȸ�
function setHeight() {
	$('.class-list li a').css({
        height: 'auto'
    });
    var maxHeight = Math.max.apply(null, $(".class-list li a").map(function () {
        return $(this).height();
    }).get());
    $('.class-list li a').css({
        height: maxHeight + 'px'
    });
}

// ������ѡ�к��л���ʽ
$(document).ready(function () {
    $(".main-nav ul a").each(function () {
        $this = $(this);
        if ($this[0].href == String(window.location)) {
            $this.addClass("current");
        }
    });
});


// ���������˵�
$(function(){ 
    var M1 = $('#dropmenu') 
    M1.on('click',function(e){e.stopPropagation();}) 
    .find('>a').on('click',function(){ 
        M1.find('>div').toggle(); 
    }); 
    $(document).on('click',function(){M1.find('>div').hide()}) 
})

// ���������˵�
$(function () {
    var Accordion = function (el, multiple) {
        this.el = el || {};
        this.multiple = multiple || false;

        // Variables privadas
        var links = this.el.find('.link');
        // Evento
        links.on('click', { el: this.el, multiple: this.multiple }, this.dropdown)
    }

    Accordion.prototype.dropdown = function (e) {
        var $el = e.data.el;
        $this = $(this),
        $next = $this.next();

        $next.slideToggle();
        $this.parent().toggleClass('open');

        if (!e.data.multiple) {
            $el.find('.submenu').not($next).slideUp().parent().removeClass('open');
        };
    }

    var accordion = new Accordion($('#accordion'), false);
});