/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Abilities } from './Abilities';
import type { AbilityName } from './AbilityName';
import type { Attack } from './Attack';
import type { CharacterClass } from './CharacterClass';
import type { CustomResource } from './CustomResource';
import type { HitDice } from './HitDice';
import type { HitPoints } from './HitPoints';
import type { Money } from './Money';
import type { Skills } from './Skills';

export type CharacterSheet = {
    classes: Array<CharacterClass>;
    abilities: Abilities;
    skills: Skills;
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
    languages_and_proficiencies: string;
    personality: string;
    ideals: string;
    bonds: string;
    flaws: string;
    features: string;
    inventory: string;
    spellcasting_ability: (AbilityName | null);
    daily_prepared_spells: number;
    exhaustion: 0 | 1 | 2 | 3 | 4 | 5 | 6;
    proficiency_bonus: number;
    ac: number;
    initiative: number;
    spell_dc: number;
    spell_attack_bonus: number;
    passive_perception: number;
};
