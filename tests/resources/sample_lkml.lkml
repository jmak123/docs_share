view: dummy {
    sql_table_name: analytics.active_users ;;
    label: "dummy"

    dimension: id {
        label: "Id"
        type: number
        description: "new docs from lkml"
        primary_key: yes
        sql: ${TABLE}.id ;;
    }

    dimension: id2 {
        label: "Id2"
        type: number
        sql: ${TABLE}.id2 ;;
    }

    dimension: id3 {
        label: "Id2"
        description: "new docs from lkml"
        type: number
        sql: ${TABLE}.id3 ;;
    }

    measure: ms {
        label: "ms"
        description: "blah"
        type: sum
        sql: ${TABLE}.ms ;;
    }

    set: basic_orgs {
        fields: [
            id,
            id2,
            ms
        ]
    }

}
