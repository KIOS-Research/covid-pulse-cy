$(document).ready(function() {
    var table = $('#datatable').dataTable({
        language: dt_language,
        order: [[ 0, "desc" ]],
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        columnDefs: [
            {orderable: true,
             searchable: true,
             className: "center",
             targets: [0, 21]
            },
            {
                data: 'Old_Case_id',
                targets: [0]
            },
            {
                data: 'Name',
                targets: [1]
            },
            {
                data: 'Surname',
                targets: [2]
            },
            {
                data: 'patient_id',
                targets: [3]
            },
            {
                data: 'Passport',
                targets: [4]
            },
            {
                data: 'Date_of_Birth',
                targets: [5]
            },
            {
                data: 'Age',
                targets: [6]
            },
            {
                data: 'District_lst',
                targets: [7]
            },
            {
                data: 'Municipality_Town_lst',
                targets: [8]
            },
            {
                data: 'PostCode_lst',
                targets: [9]
            },
            {
                data: 'Sex_lst',
                targets: [10]
            },
            {
                data: 'Phone',
                targets: [11]
            },
            {
                data: 'Ethnicity',
                targets: [12]
            },
            {
                data: 'OccupationTxt',
                targets: [13]
            },
            {
                data: 'industry_sector_lst',
                targets: [14]
            },
            {
                data: 'stays_at',
                targets: [15]
            },
            {
                data: 'Street_lst',
                targets: [16]
            },
            {
                data: 'Street_No',
                targets: [17]
            },
            {
                data: 'Address_Txt',
                targets: [18]
            },
            {
                data: 'Country_Of_Residence',
                targets: [19]
            },
            {
                data: 'Date_of_last_communication',
                targets: [20]
            },
            {
                data: 'recovered_date',
                targets: [21]
            },
        ],
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: true,
        ajax: TESTMODEL_LIST_JSON_URL
    });

    $('#datatable tbody').on('click', 'tr', function () {
    var data = table.row( this ).data();
    alert( 'You clicked on '+data[0]+'\'s row' );
    } );

});
