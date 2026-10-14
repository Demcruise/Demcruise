// Pixel-art chibi inspired by Osaragi (Sakamoto Days) — original fan-art sprite.
// Grid is 36 columns wide. Symmetric rows are written as a left half (18 cols)
// and mirrored; asymmetric parts (bowl, hands, mouth...) are overlay layers.

export const PAL: Record<string, string> = {
  K: '#1a1420', // outline
  H: '#24202c', // hair
  h: '#3d3749', // hair shine
  V: '#e9e4f2', // veil lace
  v: '#8e86a3', // veil shade over hair
  S: '#fbefe3', // skin
  s: '#eccfbd', // skin shade
  P: '#f3a5a5', // blush
  e: '#8d8b98', // iris ring
  E: '#2b2a35', // pupil
  w: '#ffffff', // highlight
  D: '#2b2639', // sheer dress
  d: '#453f57', // dress mesh light
  x: '#151219', // dress pattern lines
  B: '#f6f7fb', // bowl white
  b: '#2f50a8', // bowl blue
  c: '#c9d2ea', // bowl shade
  N: '#f6e2a0', // noodles
  n: '#d9bf74', // noodle shade
  C: '#3b2a22', // chopsticks
  R: '#b8434a', // open mouth
  O: '#fff4df', // sticker outline
};

const HALF = [
  '............KKKKKK',
  '.........KKKVvvHHH',
  '.......KKVvHHHHHHH',
  '......KVvHHHHHHHHH',
  '.....KVvHHhhHHHHHH',
  '....KVvHHHHHhhHHHH',
  '....KVHHHHHHHHHHHH',
  '...KVvHHHHHHHHHHHH',
  '...KVHHHHKKKKKKKKK',
  '..KVvHHHKSSSSSSSSS',
  '..KVHHHKSSeeeeSSSS',
  '..KVHHHKSeEEEEeSSS',
  '..KVHHHKSeEwEEeSSS',
  '..KVHHHKSeEEEEeSSS',
  '..KVHHHKSSeeeeSSSS',
  '.KVvHHHKsPPSSSSSSS',
  '.KVHHHHKSSSSSSSSSS',
  '.KVHHHHHKSSSSSSSSS',
  '.KVHHHHHHKsSSSSSSS',
  '.KVHHHHHHHKKKKKSSS',
  '.KVHHHHHHKDDDDDxDD',
  '.KVHHHHHKDDdDDDDxD',
  'KVvHHHHKDDdDxDDDDx',
  'KVHHHHKDdDDDDxDDDD',
  'KVHHHHKDDDxDDDDxDD',
  'KVHHHHKDDxDDDDDDxD',
  'KVHHHHKDDDDdDDDDDD',
  'KVHHHHKDDDDDDdDDDD',
  'KVHHHKDDDDDDDDDDDD',
  'KVHHHKDDDDDDDDDDDD',
  'KHHHHKDDDDDDDDDDDD',
  'KHHHHKDDDDDDDDDDDD',
];

const norm = (r: string) => r.padStart(18, '.').slice(-18);
export const BASE: string[] = HALF.map((h) => {
  const l = norm(h);
  return l + l.split('').reverse().join('');
});

export type Layer = {rows: string[]; x: number; y: number};

export const BOWL: Layer = {
  x: 11,
  y: 22,
  rows: [
    '.KKKKKKKKKKKK.',
    'KcNnNNnNNnNNcK',
    'KBBBBBBBBBBBBK',
    'KbbbbbBBbbbbbK',
    'KbbbbBBBBbbbbK',
    '.KbbbbBBbbbbK.',
    '..KBBBBBBBBK..',
    '...KKKKKKKK...',
  ],
};

export const LEFT_HAND: Layer = {x: 24, y: 24, rows: ['KSSK', 'SSSK', 'SSSK', 'KKK.']};

export const BLINK_L: Layer = {x: 9, y: 10, rows: ['SSSSSS', 'SSSSSS', 'SKKKKS', 'SSKKSS', 'SSSSSS']};
export const BLINK_R: Layer = {x: 21, y: 10, rows: ['SSSSSS', 'SSSSSS', 'SKKKKS', 'SSKKSS', 'SSSSSS']};

// mouths (centered under the nose line)
export const MOUTH_POUT_A: Layer = {x: 16, y: 16, rows: ['.KK.', 'K..K', '.KK.']};
export const MOUTH_POUT_B: Layer = {x: 16, y: 16, rows: ['K..K', '.KK.', '....']};
export const MOUTH_OPEN: Layer = {x: 16, y: 16, rows: ['.KK.', 'KRRK', '.KK.']};
export const MOUTH_IDLE: Layer = {x: 17, y: 16, rows: ['KK']};

// puffed cheeks while chewing: bulge the face outline by one pixel
export const CHEEKS: Layer[] = [
  {x: 6, y: 15, rows: ['KS', 'KP', 'KS']},
  {x: 28, y: 15, rows: ['SK', 'PK', 'SK']},
];
