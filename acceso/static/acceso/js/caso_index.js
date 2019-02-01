$(function() {
    $("#jsGrid").jsGrid({
        height: "100%",
        width: "100%",
        filtering: true,
        sorting: true,
        paging: true,
        autoload: true,
        pageSize: 10,
        pageButtonCount: 5,
        controller: {
            loadData: function(filter) {
                var d = $.Deferred();
                $.ajax({
                    type: "GET",
                    // TODO: As noted in views.py, I think we should explicitly include
                    // the case number in the URL. 
                    url: "/acceso/api",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { id: item.pk });
                    }));
                });
                return d.promise();
            },
        },
        fields: [
            { name: "nombre_del_caso", type: "text", width: 150 },
            { name: "descripción", type: "text", width: 300 },
        ]
    });
});
