$(document).ready (function () {
    if ($("#is_friend").val() === 'True') {
        $("#follow").hide();
    } else {
        $("#unfollow").hide();
    }
});

