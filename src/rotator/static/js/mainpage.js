$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})


$(function () {
    if ($(".alert-danger") != null && $(".alert-danger").length > 0) {
        $(".back-btn").attr("disabled", true)
    }
});

$("#logout-btn").click(function () {
    $.get("http://log:out@" + window.location.host);
    location.reload(true);
});

$(".btn-delete").click(function () {
    var backId = $(this).data('backid');
    var parent = $(this).closest("tr");
    $.post("http://" + window.location.host + "/delete/" + backId, function (data) {
        data = JSON.parse(data);
        if (data.status == "ok") {
            parent.remove();
            var alrt = document.createElement("div");
            alrt.className = "alert alert-success";
            $(alrt).attr("role", "alert");
            alrt.innerHTML = "<strong>Udało się!</strong> Plik usunięty."
            $("#main-container").prepend(alrt);
        } else {
            var alrt = document.createElement("div");
            alrt.className = "alert alert-warning";
            $(alrt).attr("role", "alert");
            alrt.innerHTML = "<strong>Nie można usunąć pliku: " + data.file + "!</strong>."
            $("#main-container").prepend(alrt);
        }
    });

});

%(".open-settingsModal").click(function () {
    $.post("http://" + window.location.host + "/settings", function (data) {

    });
});

$("#confirmBtn").click(function () {
    $.ajax({
        url: '/settings',
        type: 'PUT',
        data: 'data',
        success: function(result) {

        }
    });
});
//
//function deleteItem(id) {
//    $.post("/delete/" + id);
//    $("#link-" + id).remove();
//}
//
//$(".delete-link").click(function () {
//    var id = $(this).data('id');
//    $(this).parent().slideUp(300, function () {
//        deleteItem(id)
//    });
//
//});
//
