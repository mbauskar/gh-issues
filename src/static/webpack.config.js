const path = require('path');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

// Config directories
const OUTPUT_DIR = path.resolve(__dirname, 'build');
const SRC_DIR = path.resolve(__dirname, 'js');

// Any directories you will be adding code/files into, need to be added to this 
// array so webpack will pick them up
const defaultInclude = [SRC_DIR];

module.exports = {
	entry: {
		'gh_issues': SRC_DIR + '/index.js'
	},
	output: {
		path: OUTPUT_DIR,
		filename: '[name].react-compiled.js'
	},
	resolve: {
		modules: [path.join(__dirname, 'src'), 'node_modules'],
		extensions: ['.js', '.jsx']
	},
	module: {
		rules: [
			{
				test: /\.(scss|css)$/,
				use: ExtractTextPlugin.extract({
					fallback: 'style-loader',
					use: 'css-loader'
				})
			},
			{
				test: /\.(js|jsx)?$/,
				use: [{
					loader: 'babel-loader',
					options: {
						babelrc: true,
						presets: [ '@babel/preset-env', '@babel/preset-react' ],
						plugins: [ '@babel/plugin-proposal-class-properties', '@babel/plugin-transform-runtime']
					}
				}],
				include: defaultInclude
			},
			{
				test: /\.(jpe?g|png|gif)$/,
				use: [{ loader: 'file-loader?name=img/[name]__[hash:base64:5].[ext]' }],
				include: defaultInclude
			},
			{
				test: /\.(eot|svg|ttf|woff|woff2)$/,
				use: [{ loader: 'file-loader?name=font/[name]__[hash:base64:5].[ext]' }],
				include: defaultInclude
			}
		]
	},
	plugins: [
		new ExtractTextPlugin('gh_issues.prod.css'),
	],
	optimization: {
		runtimeChunk: 'single', // enable "runtime" chunk
		splitChunks: {
			cacheGroups: {
				vendor: {
					test: /[\\/]node_modules[\\/]/,
					name: 'vendor',
					chunks: 'all'
				}
			}
		},
		minimizer: [
			new UglifyJsPlugin({
				sourceMap: true,
				uglifyOptions: {}
			}),
			new OptimizeCSSAssetsPlugin({})
		]
	},
	devtool: 'source-map'
};