<?php
/**
 * Niementyvi Child theme functions.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'NIEMENTYVI_CHILD_VERSION', '1.0.1' );

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style(
		'niementyvi-fonts',
		'https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Rubik:wght@400;500;600;700&display=swap',
		array(),
		null
	);
	wp_enqueue_style(
		'niementyvi-child',
		get_stylesheet_uri(),
		array(),
		NIEMENTYVI_CHILD_VERSION
	);
	wp_enqueue_style(
		'niementyvi-design',
		get_stylesheet_directory_uri() . '/assets/css/niementyvi.css',
		array( 'niementyvi-child' ),
		NIEMENTYVI_CHILD_VERSION
	);
	wp_enqueue_script(
		'niementyvi-bees',
		get_stylesheet_directory_uri() . '/assets/js/bees.js',
		array(),
		NIEMENTYVI_CHILD_VERSION,
		true
	);
}, 20 );
