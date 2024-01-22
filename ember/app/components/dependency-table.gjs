import Component from '@glimmer/component';

import { DependencyCell } from './cells';
import Table from './table';

export default class DependencyTable extends Component {
  get data() {
    return this.args.dependencies.map((dependency) => ({
      values: {
        name: <template>
          <DependencyCell @dependency={{dependency}} />
        </template>,
        provider: dependency.provider,
      },
    }));
  }
  <template>
    <Table
      @data={{this.data}}
      @fallback='Found no matching dependencies'
      as |t|
    >
      <t.head />
      <t.body />
    </Table>
  </template>
}
