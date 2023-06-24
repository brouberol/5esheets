/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CharacterSchemaNoPartyNoData } from "./CharacterSchemaNoPartyNoData";

/**
 * A party details, including the members
 */
export type DisplayPartySchema = {
  id: number;
  name: string;
  members: Array<CharacterSchemaNoPartyNoData>;
};
