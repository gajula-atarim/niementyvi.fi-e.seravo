/**
 * Niementyven tila – decorative motion for the Elementor build.
 *
 * 1. Marquees: any Elementor element with the CSS class "nt-marquee" has its
 *    items (Icon List items, or the widgets inside a container) duplicated into
 *    a scrolling track. Content stays fully editable in Elementor.
 * 2. Bees: any container with the CSS class "nt-bees-hero" or "nt-bees-story"
 *    gets an animated bee layer injected behind pointer events.
 */
( function () {
	'use strict';

	if ( document.body.classList.contains( 'elementor-editor-active' ) ) {
		return;
	}

	var SVG_NS = 'http://www.w3.org/2000/svg';

	/* ---------- Marquees ---------- */
	function initMarquee( el ) {
		if ( el.dataset.ntMarquee ) {
			return;
		}
		el.dataset.ntMarquee = '1';

		var track = el.querySelector( '.elementor-icon-list-items' );
		if ( ! track ) {
			var host = el.querySelector( ':scope > .e-con-inner' ) || el;
			track = document.createElement( 'div' );
			while ( host.firstChild ) {
				track.appendChild( host.firstChild );
			}
			host.appendChild( track );
		}
		track.classList.add( 'nt-marquee__track' );

		var originals = Array.prototype.slice.call( track.children );
		for ( var r = 0; r < 2; r++ ) {
			originals.forEach( function ( node ) {
				var copy = node.cloneNode( true );
				copy.setAttribute( 'aria-hidden', 'true' );
				track.appendChild( copy );
			} );
		}
		el.classList.add( 'nt-marquee--running' );
	}

	/* ---------- Bees ---------- */
	function svg( tag, attrs, children ) {
		var node = document.createElementNS( SVG_NS, tag );
		Object.keys( attrs || {} ).forEach( function ( k ) {
			node.setAttribute( k, attrs[ k ] );
		} );
		( children || [] ).forEach( function ( c ) {
			if ( c ) {
				node.appendChild( c );
			}
		} );
		return node;
	}

	var STROKE = '#3B2A1A';

	function beeBody( w ) {
		return svg( 'g', { transform: 'scale(' + ( w / 64 ) + ') translate(-32 -36)' }, [
			svg( 'g', { 'class': 'nt-wing' }, [
				svg( 'ellipse', { cx: 24, cy: 18, rx: 11, ry: 8, fill: '#fff', 'fill-opacity': '.9', stroke: STROKE, 'stroke-width': 2.2, transform: 'rotate(-30 24 18)' } ),
				svg( 'ellipse', { cx: 37, cy: 15, rx: 9, ry: 7, fill: '#fff', 'fill-opacity': '.9', stroke: STROKE, 'stroke-width': 2.2, transform: 'rotate(25 37 15)' } )
			] ),
			svg( 'ellipse', { cx: 32, cy: 38, rx: 16, ry: 13, fill: '#F2B23B', stroke: STROKE, 'stroke-width': 2.2 } ),
			svg( 'path', { d: 'M26 27 Q23 38 26 50', stroke: STROKE, 'stroke-width': 4.5, fill: 'none' } ),
			svg( 'path', { d: 'M35 26 Q32 38 35 51', stroke: STROKE, 'stroke-width': 4.5, fill: 'none' } ),
			svg( 'circle', { cx: 44, cy: 35, r: 2, fill: STROKE } ),
			svg( 'path', { d: 'M45 28 Q48 21 52 20 M47 30 Q52 25 56 26', stroke: STROKE, 'stroke-width': 1.8, fill: 'none', 'stroke-linecap': 'round' } )
		] );
	}

	var KT = '0;0.8;0.92;1';

	function anim( tag, attrs, children ) {
		attrs.repeatCount = 'indefinite';
		return svg( tag, attrs, children );
	}

	function makeLayer( flights, pfx, viewBox, par ) {
		var defs = svg( 'defs' );
		var root = svg( 'svg', { viewBox: viewBox, preserveAspectRatio: par, 'aria-hidden': 'true', focusable: 'false' }, [ defs ] );

		flights.forEach( function ( f, i ) {
			var pid = pfx + 'p' + i;
			var begin = ( f.begin !== undefined ? f.begin : -( i * 1.7 ) ) + 's';
			var dur = f.dur + 's';
			defs.appendChild( svg( 'path', { id: pid, d: f.d } ) );

			if ( ! f.trail ) {
				var g = svg( 'g', {}, [
					anim( 'animateMotion', { dur: dur, begin: begin, rotate: 'auto' }, [ svg( 'mpath', { href: '#' + pid } ) ] ),
					beeBody( f.w )
				] );
				root.appendChild( g );
				return;
			}

			var mid = pfx + 'm' + i;
			defs.appendChild( svg( 'mask', { id: mid, maskUnits: 'userSpaceOnUse', x: -200, y: -200, width: 1840, height: 960 }, [
				svg( 'path', { d: f.d, fill: 'none', stroke: '#fff', 'stroke-width': 10, pathLength: 1, 'stroke-dasharray': '1 1', 'stroke-dashoffset': 1 }, [
					anim( 'animate', { attributeName: 'stroke-dashoffset', values: '1;0;0;0', keyTimes: KT, dur: dur, begin: begin } )
				] )
			] ) );

			root.appendChild( svg( 'g', {}, [
				svg( 'g', { mask: 'url(#' + mid + ')' }, [
					svg( 'path', { d: f.d, fill: 'none', stroke: '#333', 'stroke-width': 1.6, 'stroke-dasharray': '6 5', 'stroke-linecap': 'round' } ),
					anim( 'animate', { attributeName: 'opacity', values: '1;1;1;0', keyTimes: KT, dur: dur, begin: begin } )
				] ),
				svg( 'g', {}, [
					anim( 'animate', { attributeName: 'opacity', values: '1;1;1;0', keyTimes: KT, dur: dur, begin: begin } ),
					anim( 'animateMotion', { dur: dur, begin: begin, rotate: 'auto', keyPoints: '0;1;1;1', keyTimes: KT, calcMode: 'linear' }, [ svg( 'mpath', { href: '#' + pid } ) ] ),
					beeBody( f.w )
				] )
			] ) );
		} );

		return root;
	}

	var HERO_FLIGHTS = [
		{ trail: true, d: 'M40 640 C 60 540, 180 560, 150 490 C 120 430, 40 470, 80 520 C 120 560, 200 500, 215 465', dur: 8, w: 28, begin: -1 },
		{ trail: true, d: 'M780 640 C 730 550, 620 520, 650 450 C 680 380, 780 420, 745 475 C 710 525, 630 440, 680 330 S 725 240, 690 205', dur: 10, w: 46, begin: -4 },
		{ trail: true, d: 'M-60 60 C 80 20, 160 120, 240 80 C 320 40, 335 135, 280 132 C 225 128, 260 55, 360 50 S 520 80, 600 112', dur: 11, w: 28, begin: -7 },
		{ trail: true, d: 'M1520 380 C 1400 300, 1300 420, 1240 360 C 1180 300, 1260 240, 1300 290 C 1340 340, 1180 390, 1080 300', dur: 9, w: 30, begin: -2.5 },
		{ trail: false, d: 'M200 120 C 400 0, 560 200, 420 260 C 300 310, 120 240, 200 120 Z', dur: 12, w: 20 },
		{ trail: false, d: 'M900 150 C 1050 50, 1250 150, 1150 260 C 1050 360, 850 300, 900 150 Z', dur: 10, w: 22 },
		{ trail: false, d: 'M1100 420 C 1250 360, 1400 470, 1300 530 C 1200 590, 1000 520, 1100 420 Z', dur: 9, w: 24 },
		{ trail: false, d: 'M600 450 C 700 380, 860 470, 780 530 C 700 590, 520 520, 600 450 Z', dur: 8, w: 20 },
		{ trail: false, d: 'M100 300 C 300 100, 500 500, 720 300 C 940 100, 1140 500, 1340 300 C 1140 100, 940 500, 720 300 C 500 100, 300 500, 100 300 Z', dur: 24, w: 24 },
		{ trail: false, d: 'M1250 80 C 1380 20, 1460 160, 1340 200 C 1220 240, 1150 120, 1250 80 Z', dur: 7, w: 18 }
	];

	var STORY_FLIGHTS = [
		{ trail: true, d: 'M-40 128 C 140 178, 240 78, 380 118 C 500 153, 515 78, 455 80 C 395 82, 430 168, 620 138 S 900 88, 1060 128 S 1280 178, 1480 118', dur: 13, w: 34, begin: -2 },
		{ trail: true, d: 'M1480 660 C 1380 600, 1400 520, 1310 500 C 1230 480, 1240 570, 1300 555 C 1360 540, 1270 430, 1150 420', dur: 9, w: 26, begin: -5 },
		{ trail: false, d: 'M860 150 C 1000 90, 1160 190, 1060 250 C 960 310, 780 230, 860 150 Z', dur: 9, w: 20 },
		{ trail: false, d: 'M120 480 C 280 400, 460 520, 340 590 C 220 650, 30 560, 120 480 Z', dur: 11, w: 22 }
	];

	function addBees( el, flights, pfx, viewBox, par ) {
		if ( el.querySelector( ':scope > .nt-bees' ) ) {
			return;
		}
		var layer = document.createElement( 'div' );
		layer.className = 'nt-bees';
		layer.appendChild( makeLayer( flights, pfx, viewBox, par ) );
		el.appendChild( layer );
	}

	function init() {
		document.querySelectorAll( '.nt-marquee' ).forEach( initMarquee );
		document.querySelectorAll( '.nt-bees-hero' ).forEach( function ( el, i ) {
			addBees( el, HERO_FLIGHTS, 'nth' + i, '0 0 1440 560', 'xMidYMid slice' );
		} );
		document.querySelectorAll( '.nt-bees-story' ).forEach( function ( el, i ) {
			addBees( el, STORY_FLIGHTS, 'nts' + i, '0 0 1440 700', 'xMidYMin slice' );
		} );
	}

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', init );
	} else {
		init();
	}
} )();
