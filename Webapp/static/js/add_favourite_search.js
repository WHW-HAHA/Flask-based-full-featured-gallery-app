$(document).ready(function() {
    $(document).on('click', '.aheart', function() {
        var post_title = $(this).attr('post_title')
        var post_id = $(this).attr('post_id')

        var language = localStorage.getItem('locale') || window.navigator.language.toLowerCase() || 'en'
        if (language.indexOf("zh-") !== -1) {
        var tnum = 'cn'
        } else if (language.indexOf('en') !== -1) {
            var tnum = 'en'
        } else {
            var tnum = 'en'
        }

        var data = {'post_title': post_title,
                    'post_id': post_id,
                    'lang': tnum}
        console.log(data)

        req = $.ajax({
            url : '/search' + '/add_favourite',
            type : 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            success: function(data){},
            error: function(xhr, type) {}
        });

        req.done(function(data) {
            $('#post_content_section' + post_id).fadeOut(100).fadeIn(100);
            $('#post_content_section' + post_id).html(data);
            $(window.location.href="#popup"+ post_id);
        });
    });
});