import { hash } from '@ember/helper';
import UkModal from 'ember-uikit/components/uk-modal';

/* eslint-disable no-undef */
<template>
  <UkModal
    @visible={{@visible}}
    @bgClose={{false}}
    @escClose={{false}}
    @btnClose={{false}}
    @stack={{true}}
    as |modal|
  >
    <modal.header>
      <h2 class='uk-modal-title'>{{@title}}</h2>
    </modal.header>
    {{#if @visible}}
      {{yield
        (hash body=(component UkModal.body) footer=(component UkModal.footer))
      }}
    {{/if}}
  </UkModal>
</template>
