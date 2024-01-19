import { Input } from '@ember/component';
import { fn, get } from '@ember/helper';
import { on } from '@ember/modifier';
import Component from '@glimmer/component';
import optional from 'ember-composable-helpers/helpers/optional';
import PowerSelect from 'ember-power-select/components/power-select';
import { or } from 'ember-truth-helpers';
import { startCase } from 'lodash';

const Select = <template>
  <PowerSelect
    @options={{@options}}
    @onChange={{or @onChange (fn (mut @value))}}
    @placeholder={{@placeholder}}
    @allowClear={{true}}
    @selected={{@value}}
    id={{@name}}
    @searchField={{@searchField}}
    @searchEnabled={{@searchEnabled}}
    as |p|
  >{{or (get p (or @searchField)) p}}
  </PowerSelect>
</template>;
const Text = <template>
  <Input
    class='uk-input'
    placeholder={{@placeholder}}
    @value={{@value}}
    {{on 'change' (optional @onChange)}}
  />
</template>;

const Label = <template>
  <label for={{@name}}>{{startCase @name}}{{yield}}</label>
</template>;

export default class Dynamic extends Component {
  get component() {
    if (this.args.type === 'select') return Select;
    return Text;
  }

  <template>
    <Label @name={{@name}}>
      <this.component
        @options={{@options}}
        @placeholder={{@placeholder}}
        @onChange={{@onChange}}
        @value={{@value}}
        @name={{@name}}
        @searchEnabled={{@searchEnabled}}
        @searchField={{@searchField}}
      />
    </Label>
  </template>
}
