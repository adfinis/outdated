import { LinkTo } from '@ember/routing';

<template>
  <div
    class='navbar'
    uk-sticky='sel-target: .navbar-container; cls-active: uk-navbar-sticky'
  >
    <nav class='navbar-container' uk-navbar>
      <div class='uk-navbar-left'>
        <LinkTo @route='projects' class='uk-navbar-item uk-logo'>
          Outdated
        </LinkTo>
      </div>
      <div class='uk-navbar-right'>
        <ul class='uk-navbar-nav uk-navbar-left'>
          <div class='uk-navbar-left'></div>
        </ul>
      </div>
    </nav>
  </div>
</template>
