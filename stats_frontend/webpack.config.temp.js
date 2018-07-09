var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker')


var developmentSettings = {
    //turns options CLI params into
    //str
    args: process.argv.slice(2),
    getMode: function(){
        if (this.args === 'production'){
            return 'production';
        }
        // using ENV Variable from django portion of app
        // to check if running on production server
        else if (process.env.DJANGO_DEBUG_FALSE){
            return 'production';
        }
        else{
            return 'development'
        }
    },
    getOutput: function(){
        if (this.getMode()==='production'){
            return {
                //consider just doing 
                //path.resolve('/assets/bundles/')
                path: path.join(__dirname, 
                    'assets/bundles/'),
                filename: '[name]-[hash].js',
            }
        }
        else{
            return {
                path: path.join(__dirname, 
                    'assets/development_bundles/'),
                filename: 'app.js',
            }
        }
    }
};
module.exports = {
    context:__dirname,
    /* entry is the same in production and development hence
       the entry setting with a string (as opposed to using 
       developmentSettings.SOMEFUNCTION()) */
    entry: './assets/js/index',
    mode: 'development',
    /*  under current configuration Django will store 
        both entry and output files in static folder.
        One way to avoid this is to change .assets/bundles
        to ./assets/output/bundles, and to then collectstatic
        from ./assets/output
    */  
    output: {
        path: path.join(__dirname, 
            'assets/development_bundles/'),
        filename: 'app.js',
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        /* // Makes jQuery available to every plugin
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': jquery
        })
        */
    ]
    ,
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
    devServer:{
        compress: false,
        port: 8080,
        publicPath: '/assets/'
    }
};
