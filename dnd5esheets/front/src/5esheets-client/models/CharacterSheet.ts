/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Attack } from './Attack';
import type { CustomResource } from './CustomResource';
import type { HitDice } from './HitDice';
import type { HitPoints } from './HitPoints';
import type { Money } from './Money';
import type { Proficiencies } from './Proficiencies';
import type { Scores } from './Scores';
import type { Spells } from './Spells';

export type CharacterSheet = {
    scores: Scores;
    proficiencies: Proficiencies;
    xp: number;
    race: string;
    background: string;
    alignment: string;
    darkvision: boolean;
    inspiration: boolean;
    speed: number;
    hp: HitPoints;
    hit_dice: HitDice;
    money: Money;
    custom_resources: Array<CustomResource>;
    attacks: Array<Attack>;
    equipment: string;
    languages_and_proficiencies: string;
    personality: string;
    ideals: string;
    bonds: string;
    features: string;
    spells: Spells;
};

