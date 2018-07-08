var path = require('path');
var webpack = require('webpack');


module.exports = {
    context:__dirname,
    entry: './assets/js/index',
    mode: 'development', // change to system variable in future
    output: {
        path: path.resolve('./assets/bundles/'),
        filename: '[name]-[hash].js',
    },
    module: {
        rules:[
          {
            test: /\.(js|jsx)$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            options: {
                // babelrc: false,
                presets: ["react", "es2015"]
            },
          }
        ]
    },
    resolve: {
        extensions: ['*', '.js', '.jsx']
    },
};
