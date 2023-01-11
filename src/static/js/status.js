function updateStatus() {
    $.ajax({
        type: "GET",
        url: "/status",
        success: function (data) {
            $(".status").text(data);
            // console.log(data);
        }
    });
}

$(() => {
    updateStatus();
    setInterval(() => {
        updateStatus();
    }, 3500);
})