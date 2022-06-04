$( document ).ready(function() {
    $.ajax({
        type: 'POST',
        url:  '/get_data',
        contentType: false,
        cache: false,
        processData: false
    }).done((data,xhr)=>{
        $("#display").empty();
        var clean_data = []
        $('#display').append('<table id="tb" class=" table  text-left"></table>')
            data.map((row)=>{
            clean_data.push([row.id,row.title,row.url,row.page_language,row.length,row.alias,row.lables,row.description,row.longitude,row.latitude,row.logo,row.info])
        });
        $('#tb').DataTable( {
        data: clean_data,
        autoWidth: false,
        columns: [
            { title: "ID" ,width : '30px' },
            { title: "TITLE" },
            { title: "URL" },
            { title: "LANGUAGE" ,width : '10px' },
            { title: "LENGTH", width : '10px'},
            { title: "ALIAS" ,width : '90px' },
            { title: "LABLES" ,width : '90px' },
            { title: "DESCRIPTIONS" },
            { title: "LONGTITUDE" ,width : '20px' },
            { title: "LATITUDE",width : '20px'  } ,
            { title: "LOGO",width : '50px'  } ,
            { title: "PAGE INFORMATIONS" }                     
        ]
        } );
    }).fail((xhr)=>{
        $("#display").empty();
        $('#display').append('<h3 class="text-danger" >ERROR LOADING THE DATA</h3>')

    });
});