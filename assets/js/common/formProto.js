require("jquery");
var errors = require("errors");
var _ = require('underscore');

module.exports = {
    onAuthFailure: function(err) {
        if (err instanceof errors.AuthFailure) {
            window.location = "/welcome";
            return true;
        }
    },

    onCommonErrors: function(err) {
        if (err instanceof errors.NetworkError) {
            this.tip('网络错误!', 'danger');
            return true;
        } else if (err instanceof errors.InternalError) {
            this.tip('服务器错误!', 'danger');
            return true;
        } else if (err instanceof errors.FormInvalidError) {
            this.tip('服务器错误!', 'danger');
            return true;
        }
    },

    onUnknownError: function(err) {
        this.tip('Error!', 'danger');
        return true;
    },

    tip: function(msg, type) {
        this.$alert.hide();
        var classname = "alert-" + type;
        this.$alert.attr("class", "alert " + classname).html(msg).show();
    },

    clearTip: function() {
        this.$alert.hide().empty().attr('class', "alert");
    },

    addError: function(el, msg) {
        var $errorList = $(el).siblings('ul.parsley-error-list');
        $errorList.empty();
        $("<li>" + msg + "</li>").appendTo($errorList);
        $errorList.fadeIn();
    },

    clearError: function(el) {
        var $errorList = $(el).siblings('ul.parsley-error-list');
        $errorList.empty().hide();
    },

    clearErrors: function(fields) {
        _.each(fields, _.bind(function(field) {
            this.clearError(this.el[field]);
        }, this));
    }
};

