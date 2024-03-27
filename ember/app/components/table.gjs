import { hash, concat } from '@ember/helper';
import { service } from '@ember/service';
import { htmlSafe } from '@ember/template';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import formatDate from 'ember-intl/helpers/format-date';
import { or } from 'ember-truth-helpers';
import startCase from 'lodash/startCase';

const TableRow = <template>
  <tr>{{yield}}</tr>
</template>;

export class TableBody extends Component {
  @service intl;

  @tracked getValue = (field, { values }) => {
    const value = values[field];
    if (value instanceof Date) return <template>{{formatDate value}}</template>;
    if (value instanceof Component) return value;
    if (value === undefined || value === null) {
      return <template>
        <span class='uk-text-italic uk-text-muted'>undefined</span>
      </template>;
    }
    return <template>{{value}}</template>;
  };

  get width() {
    return 100 / this.args.fields.length;
  }

  <template>
    <tbody ...attributes>
      {{#each @data key='@index' as |value|}}
        {{#let (or value.component TableRow) as |Row|}}
          <Row>
            {{#each @fields key='@index' as |field|}}
              <td style={{htmlSafe (concat 'width:' this.width '%')}}>
                {{component (this.getValue field value)}}</td>
            {{/each}}
          </Row>
        {{/let}}
      {{/each}}
    </tbody>
  </template>
}

const TableHead = <template>
  <thead ...attributes>
    <tr>
      {{#each @fields as |field|}}
        <th>{{startCase field}}</th>
      {{/each}}
    </tr>
  </thead>
</template>;

export default class Table extends Component {
  get fields() {
    return [
      ...new Set(
        this.args.fields ??
          this.args.data.map((object) => Object.keys(object.values)).flat(),
      ),
    ];
  }

  get hasData() {
    return Boolean(this.args.data?.length);
  }

  get isVisible() {
    if (this.args.visible) return this.args.visible;
    if (this.hasData || this.args.fallback) return true;
    return false;
  }

  <template>
    {{#if this.isVisible}}
      {{#if @title}}
        <h2 class='table-header'>{{@title}}</h2>
        <hr class='seperator' />
      {{/if}}
      {{#if this.hasData}}
        <table>
          {{yield
            (hash
              body=(component TableBody fields=this.fields data=@data)
              head=(component TableHead fields=this.fields)
            )
          }}
        </table>
      {{else}}
        {{#if @fallback}}
          <div class='text-empty' data-test-fallback>
            {{@fallback}}
          </div>
        {{/if}}
      {{/if}}
    {{/if}}
  </template>
}
