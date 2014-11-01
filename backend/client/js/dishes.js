require("jquery");
require("jquery.serializeObject");
require("jquery.iframe-transport");
require("bootstrap");
//require("moment");
//require("bootstrap-datetimepicker");
//require("zh-CN");
//require("select2");
var parsley = require("parsley");
var csrf_token = require("node-django-csrf-support")();
var when = require("when/when");
var _ = require("underscore");
var Backbone = require("backbone");
Backbone.$ = $;
var SimpleUpload = require("simple-upload");

var errors = require("errors");
var utils = require("utils");
var mapErrors = utils.mapErrors;
var throwNetError = utils.throwNetError;
var handleErrors = utils.handleErrors;
var formProto = require("formProto");
//var formValidationProto = require("formValidationProto");
var modals = require('modals');
//var SimpleUpload = require("simple-upload");

function modifyDishes(data) {
    var request = $.post("/backend/dishes/" + data.pk, data, 'json');
    return when(request).then(mapErrors, throwNetError);
}

function addDishes(data) {
    var request = $.post("/backend/dishes/add", data, 'json');
    return when(request).then(mapErrors, throwNetError);
}

function deleteDishes(id) {
    var request = $.post("/backend/dishes/delete", {
        id: id
    }, 'json');
    return when(request).then(mapErrors, throwNetError);
}

function upload(el) {
    return when($.ajax("/qiniu_upload/", {
        method: 'POST',
        iframe: true,
        data: {
            csrfmiddlewaretoken: csrf_token
        },
        files: el,
        processData: false,
        dataType: 'json'
    })).then(function(data) {
        return mapErrors(data, function(data) {
            return data.key;
        });
    }, throwNetError);
}

function getUrl(key) {
    return key;
}

var proto = _.extend({}, formProto);
var DishesForm = Backbone.View.extend(_.extend(proto, {
    initialize: function() {
        this.setElement($.parseHTML(DishesForm.tpl().trim())[0]);
        this.$('[name=name]').attr({
            maxlength: 80
        });
        this.$fieldCover = this.$(".group-cover .cover");
        this.upload = new SimpleUpload.SimpleUpload({
            name: 'cover',
            id: 'id_cover',
            getUrl: getUrl,
            upload: upload
        });
        this.upload.on('upload-failed', _.bind(function() {
            this.$coverErrors.empty();
            $("<li>" + "pages.uploadFailed" + "</li>").appendTo(this.$coverErrors);
            this.$coverErrors.fadeIn();
        }, this)).on('upload-done', _.bind(function() {
            this.$coverErrors.empty().fadeOut();
        }, this));
        $(this.upload.el).appendTo(this.$fieldCover);
        this.$coverErrors = $("<ul class='parsley-error-list' style='display: none'></ul>");
        this.$coverErrors.appendTo(this.$fieldCover);
        this.$alert = this.$("p.alert");
        this.$(".glyphicon-info-sign").tooltip();
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
            this.el[attr].value = dishes[attr];
        }, this));
        this.upload.setPath(dishes.cover);
    },

    onShow: function() {},

    clear: function() {
        _.each(['pk', 'name', 'cover', 'price', 'desc'], _.bind(function(field) {
            $(this.el[field]).val('');
        }, this));

        this.clearTip();
    },

    onHide: function() {
        this.clear();
        this.clearErrors(['name', 'cover', 'price', 'desc'])
        this.upload.setPath(null);
        //$(this.el).parsley('destroy');
    },

    validate: function() {
        this.clearErrors(['name', 'cover', 'price', 'desc']);
        this.clearTip();

        if (this.el.name.value.trim() === "") {
            this.addError(this.el.name, '这是必填项。');
            return false;
        }
        if (this.el.cover.value.trim() === "") {
            this.addError(this.$('[name=coverEmpty]'), '这是必填项。');
            return false;
        }
        var price = this.el.price.value.trim();
        if (price === "") {
            this.addError(this.el.price, '这是必填项。');
            return false;
        }else if (parseFloat(price) != price || parseFloat(price) < 0) {
            this.addError(this.el.price, '请填入正数。');
            return false;
        }

        if(this.el.desc.value.trim() === ""){
            this.addError(this.el.desc, '这是必填项。');
            return false;
        }

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

        var data = this.$el.serializeObject();

        if (this.el.pk.value !== "") {
            modifyDishes(data)
                .then(onFinish, onReject)
                .ensure(onComplete);
        } else {
            addDishes(data)
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
        return deleteDishes(id).then(function() {
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
