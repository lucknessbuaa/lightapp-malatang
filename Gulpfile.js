var fs = require('fs');
var less = require('gulp-less');
var gulp = require('gulp');
var gulpif = require('gulp-if');
var util = require('gulp-util');
var changed = require('gulp-changed');
var imagemin = require('gulp-imagemin');
var merge = require('merge-stream');
var nodemon = require('gulp-nodemon');
var tinypng = require('gulp-tinypng');
var streamify = require('gulp-streamify')
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var base64 = require('gulp-base64');
var browserify = require('browserify');
var source = require('vinyl-source-stream')
var stringify = require('stringify');
var CombinedStream = require('combined-stream');
var developing = process.env.NODE_ENV === 'development';

try {
    var notify = require('display-notification');
} catch (e) {
    var notify = function() {};
}

function browserifyStream(entry, filename) {
    var b = browserify(entry);

    b.transform({
        global: true
    }, 'brfs');
    b.transform({
        global: true
    }, 'browserify-shim');

    var stream = b.bundle();
    return stream.on('error', onError(function() {
            stream.end();
        })).pipe(source(filename))
        .pipe(gulpif(!developing, streamify(uglify({
            preserveComments: 'some'
        }))));
}

function onError(fn) {
    return function(err) {
        console.error(err);
        notify({
            title: 'Error',
            subtitle: 'fail to compiling scripts',
            text: err,
            sound: 'Bottle'
        });

        if (fn) {
            fn.call(err);
        }
    }
}

gulp.task("less", function() {
    return gulp.src("backend/client/less/*.less")
        .pipe(less({
            compress: true,
            paths: ["assets", "assets/components", "assets/less"]
            }))
        .on("error", console.error)
        .pipe(gulp.dest("assets/css/backend"));
});

gulp.task('login', function() {
	return browserifyStream("./backend/client/js/login.js", "login.js")
        .pipe(gulp.dest('assets/js/backend'));

});

gulp.task('scripts', function() {
    var dishes = browserifyStream("./backend/client/js/dishes.js", "dishes.js")
        .pipe(gulp.dest('assets/js/backend'));

    var takeout = browserifyStream("./backend/client/js/takeout.js", "takeout.js")
        .pipe(gulp.dest('assets/js/backend'));

    var preorder = browserifyStream("./backend/client/js/preorder.js", "preorder.js")
        .pipe(gulp.dest('assets/js/backend'));

    var user = browserifyStream("./backend/client/js/user.js", "user.js")
        .pipe(gulp.dest('assets/js/backend'));

    return merge(dishes, takeout, preorder, user);
});

/*
gulp.task('sass', function() {
    return gulp.src("scss/*.scss")
        .pipe(sass({
            errLogToConsole: true
        }))
        .pipe(base64({
            baseDir: 'public/css',
            maxImageSize: 48 * 1024 // 48k
        }))
        .pipe(gulp.dest("public/css"));
});

gulp.task('image-png', function() {
    return gulp.src("images/*.png")
        .pipe(changed('public/img'))
        .pipe(tinypng('9kl3nT2f8qC-AaApBVXDeQt-37ArLMNs'))
        .on('error', console.error)
        .pipe(gulp.dest("public/img"));
});

gulp.task('image-other', function() {
    return gulp.src("images/*.{jpg,jpeg,gif}")
        .pipe(changed('public/img'))
        .pipe(imagemin({
            progressive: true
        }))
        .pipe(gulp.dest("public/img"));
});

gulp.task("watch-scripts", function() {
    gulp.watch(["public/index.js", "package.json"], ["scripts"]);
});

gulp.task("watch-images", function() {
    gulp.watch("images/*", ["image-png", "image-other"]);
});

gulp.task("watch-sass", function() {
    gulp.watch(["scss/*", "img/*"], ["sass"]);
});

gulp.task("watch", ["watch-sass", "watch-images", "watch-scripts"]);
*/
