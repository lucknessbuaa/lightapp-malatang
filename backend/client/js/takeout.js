require("jquery");
require("jquery.serializeObject");
require("jquery.iframe-transport");
require("bootstrap");
//require("moment");
//require("bootstrap-datetimepicker");
//require("zh-CN");
//require("select2");
//require("parsley");
var csrf_token = require("node-django-csrf-support");
var when = require("when/when");
var _ = require("underscore");
var Backbone = require("backbone");
Backbone.$ = $;

var errors = require("errors");
var utils = require("utils");
var mapErrors = utils.mapErrors;
var throwNetError = utils.throwNetError;
var handleErrors = utils.handleErrors;
var formProto = require("formProto");
//var formValidationProto = require("formValidationProto");
var modals = require('kuzhanggui-modals');
//var SimpleUpload = require("simple-upload");

function modifyTalk(data) {
    var request = $.post("/backend/talk/" + data.pk, data, 'json');
    return when(request).then(mapErrors, throwNetError);
}

function addTalk(data) {
    var request = $.post("/backend/talk/add", data, 'json');
    return when(request).then(mapErrors, throwNetError);
}

function deleteTalk(id) {
    var request = $.post("/backend/talk/delete", {
        id: id
    }, 'json');
    return when(request).then(mapErrors, throwNetError);
}

var proto = _.extend({}, formProto);
var DishesForm = Backbone.View.extend(_.extend(proto, {
    initialize: function() {
        this.setElement($.parseHTML(DishesForm.tpl().trim())[0]);
        this.$alert = this.$("p.alert");
        this.$(".glyphicon-info-sign").tooltip();
        this.$("[name=place]").attr({
            maxlength: 100
        });
    },

    bind: function(data) {
        var defaults = {
            id: '',
            title: '',
            description: '',
            url: ''
        };
        data = _.defaults(data, defaults);
        _.each(['pk', 'city', 'university', 'date', 'place', 'capacity', 'speaker', 'wtdate', 'seats', 'grabbing'], _.bind(function(attr) {
            this.el[attr].value = data[attr];
        }, this));
    },

    setDishes: function(dishes) {
        _.each(['pk', 'name', 'cover', 'price', 'desc'], _.bind(function(attr) {
            this.el[attr].value = talk[attr];
        }, this));
    },

    onShow: function() {
    },

    clear: function() {
        _.each(['pk', 'name', 'cover', 'price', 'desc'], _.bind(function(field) {
            $(this.el[field]).val('');
        }, this));

        this.clearTip();
    },

    onHide: function() {
        this.clear();
        this.clearErrors(['name', 'cover', 'price', 'desc'])
        $(this.el).parsley('destroy');
    },

    validate: function() {
        this.clearErrors(['city', 'university', 'date', 'place', 'cover', 'capacity', 'speaker', 'wtdate', 'seats', 'grabbing']);
        this.clearTip();

        if (this.el.city.value === "") {
            this.el.city.value = '1';
        }
        if (this.el.university.value === "") {
            this.el.university.value = '1';
        }
        if (this.el.date.value === "") {
            this.addError(this.el.date, '这是必填项。');
            return false;
        }
        if (this.el.place.value.trim() === "") {
            this.addError(this.el.place, '这是必填项。');
            return false;
        }
        if (this.el.cover.value.trim() === "") {
            this.addError(this.el.cover, '这是必填项。');
            return false;
        }
        capa = this.el.capacity.value;
        if (this.$("#number").is(":checked")) {
            this.el.capacity.value = 0;
        } else {
            if (capa === "" || parseInt(capa) != capa) {
                this.addError(this.el.capacity, '这是必填项/应该填入整数。');
                return false;
            }
            if (capa <= 0) {
                this.addError(this.el.capacity, '必须输入正数。');
                return false;
            }
            if (capa >= 2000) {
                this.addError(this.el.capacity, '座位数应该小于2000！');
                return false;
            }
        }

        if (!this.$("#number").prop("checked") && $(this.el.grabbing).prop("checked")) {
            var seats = this.el.seats.value;
            if (seats !== "") {
                if (!/^\d+$/.test(seats)) {
                    this.addError(this.el.seats, '这是必填项/应该填入整数。');
                    return false;
                }

                seats = parseInt(seats);
                if (seats > capa) {
                    this.addError(this.el.seats, '占座数量不应该超过总座位数量');
                    return false;
                }
            }
        }

        if (this.el.wtdate.value === "") {
            this.addError(this.el.wtdate, '这是必填项。');
            return false;
        }
        //if (this.el.wtdate.value <= this.el.date.value) {
        //    this.addError(this.el.wtdate, '笔试时间应该在宣讲会时间之后。');
        //    return false;
        //}

        return true;
    },

    save: function() {
        var onComplete = _.bind(function() {
            this.trigger('save');
        }, this);

        if (!this.validate()) {
            return setTimeout(onComplete, 0);
        }

        var onReject = _.bind(function(err) {
            handleErrors(err,
                _.bind(this.onAuthFailure, this),
                _.bind(this.onCommonErrors, this),
                _.bind(this.onUnknownError, this)
            );
        }, this);

        var onFinish = _.bind(function() {
            this.tip('成功！', 'success');
            utils.reload(500);
        }, this);

        var data = this.getData();

        if (this.el.pk.value !== "") {
            modifyTalk(data)
                .then(onFinish, onReject)
                .ensure(onComplete);
        } else {
            addTalk(data)
                .then(onFinish, onReject)
                .ensure(onComplete);
        }
    }
}));

$(function() {
    DishesForm.tpl = _.template($("#form-tpl").html());

    var form = new DishesForm();
    var modal = new modals.FormModal();
    modal.setForm(form);
    $(modal.el).appendTo(document.body);

    $create = $("#create-dishes");
    $create.click(function() {
        modal.show();
        modal.setTitle('创建菜品信息');
        modal.setSaveText("创建", "创建中...");
    });


    $("table").on("click", ".edit", function() {
        modal.setTitle('编辑菜品信息');
        modal.setSaveText("保存", "保存中...");
        var dishes = $(this).parent().data();
        form.setDishes(dishes);
        modal.show();
    });
});

$(function() {
    var modal = new modals.ActionModal();
    modal.setAction(function(id) {
        return deleteTalk(id).then(function() {
            utils.reload(500);
        }, function(err) {
            if (err instanceof errors.AuthFailure) {
                window.location = "/login";
            }

            throw err;
        });
    });
    modal.setTitle('删除菜品信息');
    modal.tip('确定要删除吗？');
    modal.setSaveText('删除', '删除中...');
    modal.on('succeed', function() {
        utils.reload(500);
    });
    $("table").on("click", ".delete", function() {
        modal.setId($(this).parent().data('pk'));
        modal.show();
    });
});
