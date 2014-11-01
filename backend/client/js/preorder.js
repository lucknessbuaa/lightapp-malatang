require("jquery");
require("jquery.serializeObject");
require("jquery.iframe-transport");
require("bootstrap");
var moment = require("moment");
require("bootstrap-datetimepicker");
require("zh-CN");
var parsley = require("parsley");
require("node-django-csrf-support")();
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
var modals = require('modals');

/*function modifyPreorder(data) {
    var request = $.post("/backend/preorder/" + data.pk, data, 'json');
    return when(request).then(mapErrors, throwNetError);
}
*/

function completePreorder(id) {
    var request = $.post("/backend/preorder/complete", {
        id: id
    }, 'json');
    return when(request).then(mapErrors, throwNetError);
}

function deletePreorder(id) {
    var request = $.post("/backend/preorder/delete", {
        id: id
    }, 'json');
    return when(request).then(mapErrors, throwNetError);
}

/*var proto = _.extend({}, formProto);
var PreorderForm = Backbone.View.extend(_.extend(proto, {
    initialize: function() {
        this.setElement($.parseHTML(PreorderForm.tpl().trim())[0]);
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
        _.each(['pk', 'start', 'end', 'number'], _.bind(function(attr) {
            this.el[attr].value = data[attr];
        }, this));
    },

    setDate: function() {
        this.$("[name=start]").attr({
            readOnly: "true"
        });
        this.$("[name=end]").attr({
            readOnly: "true"
        });
        this.$("[name=start]").datetimepicker({
            maxView: 2,
            minView: 0,
            language: 'zh-CN',
            format: 'yyyy-mm-dd hh:ii',
            viewSelect: 'month',
            autoclose: "true"
        });
        this.$("[name=end]").datetimepicker({
            maxView: 2,
            minView: 0,
            language: 'zh-CN',
            format: 'yyyy-mm-dd hh:ii',
            viewSelect: 'month',
            autoclose: "true"
        });
        this.$("[name=start]").datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        this.$("[name=end]").datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
    },

    setPreorder: function(preorder) {
        _.each(['pk', 'start', 'end', 'number'], _.bind(function(attr) {
            this.el[attr].value = preorder[attr];
        }, this));
    },

    onShow: function() {
        this.setDate();
    },

    clear: function() {
        _.each(['pk', 'start', 'end', 'number'], _.bind(function(field) {
            $(this.el[field]).val('');
        }, this));

        this.clearTip();
    },

    onHide: function() {
        this.clear();
        this.clearErrors(['start', 'end', 'number'])
        //$(this.el).parsley('destroy');
    },

    validate: function() {
        this.clearErrors(['start', 'end', 'number']);
        this.clearTip();

        if(this.el.end.value < this.el.start.value) {
            this.addError(this.el.end, '结束时间应该在起始时间之后。');
            return false;
        }

        var count = this.el.number.value.trim();
        if (count === "") {
            this.addError(this.el.number, '这是必填项，请填入正整数。');
            return false;
        }else if(count.indexOf('.') != -1 || parseInt(count) != count || parseInt(count) <= 0){
            this.addError(this.el.number, '请填入正整数。')
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

        modifyPreorder(data)
            .then(onFinish, onReject)
            .ensure(onComplete);
    }
}));

$(function() {
    PreorderForm.tpl = _.template($("#form-tpl").html());

    var form = new PreorderForm();
    var modal = new modals.FormModal();
    modal.setForm(form);
    $(modal.el).appendTo(document.body);

    $("table").on("click", ".edit", function() {
        modal.setTitle('编辑菜品信息');
        modal.setSaveText("保存", "保存中...");
        var preorder = $(this).parent().data();
        form.setPreorder(preorder);
        modal.show();
    });
});
*/

$(function() {
    var modal = new modals.ActionModal();
    modal.setAction(function(id) {
        return deletePreorder(id).then(function() {
            utils.reload(500);
        }, function(err) {
            if (err instanceof errors.AuthFailure) {
                window.location = "/login";
            }

            throw err;
        });
    });
    modal.setTitle('删除预约信息');
    modal.tip('确定要删除吗？');
    modal.setSaveText('删除', '删除中...');
    modal.on('succeed', function() {
        utils.reload(500);
    });
    $("table").on("click", ".delete", function() {
        modal.setId($(this).parent().data('pk'));
        modal.show();
    });

    var modalOk = new modals.ActionModal();
    modalOk.setAction(function(id) {
        return completePreorder(id).then(function() {
            utils.reload(500);
        }, function(err) {
            if (err instanceof errors.AuthFailure) {
                window.location = "/login";
            }

            throw err;
        });
    });
    modalOk.setTitle('修改菜品状态');
    modalOk.tip('确定将该订单的状态改为完成吗？');
    modalOk.setSaveText('保存', '保存中...');
    modalOk.on('succeed', function() {
        utils.reload(500);
    });
    $("table").on("click", ".complete", function() {
        modalOk.setId($(this).parent().data('pk'));
        modalOk.show();
    });
});
