/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { AbilityName } from './AbilityName';
import type { Spell } from './Spell';

export type Spells = {
    spellcasting_ability: (AbilityName | null);
    daily_prepared: number;
    cantrips?: Array<Spell>;
    lvl1?: Array<Spell>;
    lvl2?: Array<Spell>;
    lvl3?: Array<Spell>;
    lvl4?: Array<Spell>;
    lvl5?: Array<Spell>;
    lvl6?: Array<Spell>;
    lvl7?: Array<Spell>;
    lvl8?: Array<Spell>;
    lvl9?: Array<Spell>;
};

