$(function () {
    /*widgest 中卷起的js*/
    $('.panel-close').click(function () {
        $(this).parent().parent().parent().hide(300);
    });

    $('.collapse').on('hide.bs.collapse', function () {
        $(this).prev().find(".panel-collapse").removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
    });

    $('.collapse').on('show.bs.collapse', function () {
        $(this).prev().find(".panel-collapse").removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
    });

    /*****************返回顶部兼容性写法*********************/
    var isTop = true;
    var clientHeight = document.documentElement.clientHeight || document.body.clientHeight;

    $('.to-top').click(function () {
        var timer = setInterval(function () {
            //获取滚动条到顶部的距离
            //我们需要兼容一些浏览器的写法 所以需要使用||兼容chrome
            var osTop = document.documentElement.scrollTop || document.body.scrollTop;

            //返回一个整数
            var speed = Math.floor(-osTop / 1.5);
            //滚动事件
            isTop = true;
            //设置滚动条到顶部的距离
            //我们需要兼容一些浏览器的写法 所以需要使用||兼容chrome
            document.documentElement.scrollTop = document.body.scrollTop = osTop + speed;
            //这里必须设置为真 如果为假 在触发滚动事件的时候 就会关闭定时器
            if (osTop <= 0) {
                clearInterval(timer);
            }
        }, 50);
    });

    //滚动时发生的事件
    window.onscroll = document.onscroll = function () {
        //获取滚动条到顶部的距离
        //我们需要兼容一些浏览器的写法 所以需要使用||兼容chrome
        var osTop = document.documentElement.scrollTop || document.body.scrollTop;
        //滚动到第二屏的时候 会出现回到顶部的按钮
        if (osTop > clientHeight) {
            $('.to-top').css({
                'display': 'block'
            })
        } else {
            $('.to-top').css({
                'display': 'none'
            })
        }

        if (!isTop) {
            clearInterval();
        }
        isTop = false;
    };
    /**********************返回顶部end***************************/
});

/*提示的js*/
$(function () {
    $("[data-toggle='tooltip']").tooltip();
});
$('#nav-login').tooltip('hide');
