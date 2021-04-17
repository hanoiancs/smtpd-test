document.addEventListener("DOMContentLoaded", function(event) {
    new Vue({
        el: '#app',
        data: {
            mails: [],
            current_mail: null,
            paging: {}
        },
        mounted: function () {
            this.fetch();
        },
        methods: {
            show: function (idx) {
                this.current_mail = this.mails[idx];
            },
            fetch: function () {
                axios
                    .get('/mails?page=' + this.paging.current)
                    .then(response => {
                        if (response.status === 200) {
                            this.mails = response.data.docs;
                            this.paging = response.data.paging;
                        } else {
                            this.mails = [];
                            this.paging = {};
                        }
                    });
            },
            fetch_next: function () {
                if (this.paging.total > 1 && this.paging.current < this.paging.total) {
                    this.paging.current++;
                    this.fetch();
                }
            },
            fetch_prev: function () {
                if (this.paging.total > 1 && this.paging.current > 1) {
                    this.paging.current--;
                    this.fetch();
                }
            }
        }
    });
});