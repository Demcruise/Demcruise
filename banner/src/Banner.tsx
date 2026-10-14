import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {z} from 'zod';
import {
  BASE,
  BLINK_L,
  BLINK_R,
  BOWL,
  CHEEKS,
  LEFT_HAND,
  Layer,
  MOUTH_IDLE,
  MOUTH_OPEN,
  MOUTH_POUT_A,
  MOUTH_POUT_B,
  PAL,
} from './sprite';

export const bannerSchema = z.object({
  name: z.string(),
  subtitle: z.string(),
  roles: z.array(z.string()),
  motto: z.string(),
});
export type BannerProps = z.infer<typeof bannerSchema>;

const W = 1200;
const H = 400;
const INK = '#1a1420';
const MONO = "Consolas, 'Cascadia Mono', ui-monospace, monospace";
const EAT_CYCLE = 120; // frames per bite

// ---------------------------------------------------------------- helpers ---
const Pixels: React.FC<{rows: string[]; px: number; x?: number; y?: number}> = ({rows, px, x = 0, y = 0}) => (
  <>
    {rows.flatMap((row, ry) => {
      const out: React.ReactNode[] = [];
      let cx = 0;
      while (cx < row.length) {
        const c = row[cx];
        if (c === '.') {
          cx++;
          continue;
        }
        let run = 1;
        while (row[cx + run] === c) run++;
        out.push(
          <rect key={`${ry}-${cx}`} x={(x + cx) * px} y={(y + ry) * px} width={run * px} height={px} fill={PAL[c]} />,
        );
        cx += run;
      }
      return out;
    })}
  </>
);

const L: React.FC<{layer: Layer; px: number}> = ({layer, px}) => (
  <Pixels rows={layer.rows} px={px} x={layer.x} y={layer.y} />
);

// Bresenham line on the sprite grid
const line = (x0: number, y0: number, x1: number, y1: number) => {
  const pts: [number, number][] = [];
  const dx = Math.abs(x1 - x0);
  const dy = -Math.abs(y1 - y0);
  const sx = x0 < x1 ? 1 : -1;
  const sy = y0 < y1 ? 1 : -1;
  let err = dx + dy;
  for (;;) {
    pts.push([x0, y0]);
    if (x0 === x1 && y0 === y1) break;
    const e2 = 2 * err;
    if (e2 >= dy) {
      err += dy;
      x0 += sx;
    }
    if (e2 <= dx) {
      err += dx;
      y0 += sy;
    }
  }
  return pts;
};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// ----------------------------------------------------------- pixel glyphs ---
const GLYPHS: Record<string, string[]> = {
  D: ['1110', '1001', '1001', '1001', '1001', '1001', '1110'],
  E: ['1111', '1000', '1000', '1110', '1000', '1000', '1111'],
  M: ['10001', '11011', '10101', '10101', '10001', '10001', '10001'],
  C: ['0111', '1000', '1000', '1000', '1000', '1000', '0111'],
  R: ['1110', '1001', '1001', '1110', '1010', '1001', '1001'],
  U: ['1001', '1001', '1001', '1001', '1001', '1001', '0110'],
  I: ['111', '010', '010', '010', '010', '010', '111'],
  S: ['0111', '1000', '1000', '0110', '0001', '0001', '1110'],
};

const PixelWord: React.FC<{word: string; px: number; fill: string; frame: number}> = ({word, px, fill, frame}) => {
  let x = 0;
  const rects: React.ReactNode[] = [];
  word.split('').forEach((ch, i) => {
    const g = GLYPHS[ch];
    if (!g) {
      x += 3 * px;
      return;
    }
    // each letter hops in a little wave
    const hop = Math.round(Math.sin(((frame - i * 6) / 40) * Math.PI * 2) * 1.2) * (px / 2);
    g.forEach((row, ry) =>
      row.split('').forEach((v, rx) => {
        if (v === '1')
          rects.push(<rect key={`${i}-${ry}-${rx}`} x={x + rx * px} y={ry * px - hop} width={px} height={px} fill={fill} />);
      }),
    );
    x += g[0].length * px + px;
  });
  return <>{rects}</>;
};

// ------------------------------------------------------------- background ---
const Background: React.FC = () => {
  const bands = ['#e9787f', '#ec8a83', '#ef9c86', '#f2ae88', '#f3bf88', '#f4cd86', '#f5d983'];
  const bh = 320 / bands.length;
  const dots: React.ReactNode[] = [];
  const gap = 34;
  for (let row = 0; row * gap < 340; row++) {
    for (let col = 0; col * gap < W + gap; col++) {
      const cx = col * gap + (row % 2 ? gap / 2 : 0);
      const cy = row * gap + 10;
      dots.push(<circle key={`${row}-${col}`} cx={cx} cy={cy} r={12} fill="#fff" opacity={0.16} />);
    }
  }
  return (
    <>
      {bands.map((c, i) => (
        <rect key={c} x={0} y={i * bh} width={W} height={bh + 1} fill={c} />
      ))}
      {dots}
    </>
  );
};

const Table: React.FC = () => {
  const grain: React.ReactNode[] = [];
  for (let i = 0; i < 9; i++) {
    const y = 336 + i * 8;
    grain.push(<rect key={i} x={(i * 173) % 400} y={y} width={W} height={2} fill="#b8a27c" opacity={0.55} />);
  }
  return (
    <>
      <rect x={0} y={318} width={W} height={82} fill="#cdb995" />
      <rect x={0} y={318} width={W} height={6} fill="#e3d4b3" />
      <rect x={0} y={324} width={W} height={3} fill="#a8916b" />
      {grain}
    </>
  );
};

// ------------------------------------------------------------------ sprite ---
const Osaragi: React.FC<{frame: number; px: number}> = ({frame, px}) => {
  const t = frame % EAT_CYCLE;

  // chopstick hand path: bowl -> mouth -> bowl
  const up = interpolate(t, [8, 28], [0, 1], clamp);
  const down = interpolate(t, [40, 54], [0, 1], clamp);
  const k = up - down; // 0 at bowl, 1 at mouth
  const hand = {x: Math.round(interpolate(k, [0, 1], [8, 11])), y: Math.round(interpolate(k, [0, 1], [24, 19]))};
  const tip = {x: Math.round(interpolate(k, [0, 1], [15, 17])), y: Math.round(interpolate(k, [0, 1], [23, 17]))};
  const dipping = t < 8 && Math.floor(t / 4) % 2 === 1;

  const carrying = t >= 8 && t < 36;
  const noodleLen = t < 30 ? 4 : Math.max(0, 4 - (t - 30));
  const mouthOpen = t >= 24 && t < 38;
  const chewing = t >= 54 && t < EAT_CYCLE - 4;
  const chewPhase = Math.floor((t - 54) / 6) % 2;
  const blink = (frame % 240 >= 92 && frame % 240 < 97) || (frame % 240 >= 200 && frame % 240 < 204);
  const bob = chewing && chewPhase === 1 ? 1 : 0;

  const sticks = [...line(hand.x + 2, hand.y, tip.x, tip.y + (dipping ? 1 : 0)), ...line(hand.x + 3, hand.y + 1, tip.x + 1, tip.y + 1 + (dipping ? 1 : 0))];

  const mouth = mouthOpen ? MOUTH_OPEN : chewing ? (chewPhase ? MOUTH_POUT_B : MOUTH_POUT_A) : MOUTH_IDLE;

  return (
    <g transform={`translate(0 ${bob * px})`}>
      <Pixels rows={BASE} px={px} />
      {blink && (
        <>
          <L layer={BLINK_L} px={px} />
          <L layer={BLINK_R} px={px} />
        </>
      )}
      {chewing && CHEEKS.map((c, i) => <L key={i} layer={c} px={px} />)}
      <L layer={mouth} px={px} />
      <L layer={BOWL} px={px} />
      <L layer={LEFT_HAND} px={px} />
      {sticks.map(([x, y], i) => (
        <rect key={`s${i}`} x={x * px} y={y * px} width={px} height={px} fill={PAL.C} />
      ))}
      {carrying &&
        noodleLen > 0 &&
        [0, 1].map((s) =>
          Array.from({length: noodleLen - s}, (_, j) => (
            <rect key={`n${s}-${j}`} x={(tip.x + s) * px} y={(tip.y + 1 + j) * px} width={px} height={px} fill={j % 2 ? PAL.n : PAL.N} />
          )),
        )}
      {/* chopstick hand */}
      <Pixels rows={['KSSK', 'SSSS', 'KSSK', '.KK.']} px={px} x={hand.x} y={hand.y} />
    </g>
  );
};

// ------------------------------------------------------------- side items ---
const Sparkle: React.FC<{x: number; y: number; frame: number; delay: number; color: string}> = ({x, y, frame, delay, color}) => {
  const p = (frame + delay) % 60;
  const s = p < 30 ? Math.floor(p / 10) : Math.max(0, 2 - Math.floor((p - 30) / 10));
  const arm = [2, 5, 8][s];
  return (
    <g opacity={s === 0 ? 0.5 : 1}>
      <rect x={x - arm} y={y - 2} width={arm * 2} height={4} fill={color} />
      <rect x={x - 2} y={y - arm} width={4} height={arm * 2} fill={color} />
    </g>
  );
};

const Typing: React.FC<{roles: string[]; frame: number}> = ({roles, frame}) => {
  const per = 240 / roles.length;
  const idx = Math.floor(frame / per) % roles.length;
  const local = frame % per;
  const word = roles[idx];
  const typeEnd = per * 0.4;
  const eraseStart = per * 0.82;
  const shown =
    local < typeEnd
      ? Math.ceil((local / typeEnd) * word.length)
      : local < eraseStart
        ? word.length
        : Math.floor((1 - (local - eraseStart) / (per - eraseStart)) * word.length);
  const cursorOn = Math.floor(frame / 8) % 2 === 0;
  const text = word.slice(0, Math.max(0, shown));
  return (
    <g transform="translate(70 214)">
      <rect x={0} y={0} width={430} height={56} fill="#fffaf2" stroke={INK} strokeWidth={4} />
      <rect x={6} y={56} width={430} height={6} fill={INK} />
      <rect x={430} y={6} width={6} height={56} fill={INK} />
      <text x={20} y={37} fontFamily={MONO} fontSize={26} fill="#e9787f" fontWeight={700}>
        &gt;
      </text>
      <text x={46} y={37} fontFamily={MONO} fontSize={26} fill={INK} fontWeight={700}>
        {text}
      </text>
      {cursorOn && <rect x={46 + text.length * 14.3 + 2} y={14} width={13} height={28} fill="#2f50a8" />}
    </g>
  );
};

const Nom: React.FC<{frame: number; x: number; y: number}> = ({frame, x, y}) => {
  const t = frame % EAT_CYCLE;
  if (t < 58 || t > EAT_CYCLE - 8) return null;
  const rise = Math.floor((t - 58) / 6) * 2;
  const show = Math.floor((t - 58) / 18) % 2 === 0 ? 'nom' : 'nom nom';
  return (
    <g transform={`translate(${x} ${y - rise})`}>
      <text fontFamily={MONO} fontWeight={700} fontSize={22} fill="#fff" stroke={INK} strokeWidth={5} paintOrder="stroke">
        {show}
      </text>
    </g>
  );
};

// ------------------------------------------------------------------ banner ---
export const Banner: React.FC<BannerProps> = ({name, subtitle, roles, motto}) => {
  const frame = useCurrentFrame();
  const px = 9;
  const charW = 36 * px;
  const charX = 790;
  const charY = 318 - 31 * px; // sit behind the table edge
  return (
    <AbsoluteFill>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} shapeRendering="crispEdges">
        <Background />

        {/* title block */}
        <g transform="translate(76 64)">
          <PixelWord word={name} px={10} fill="#fffaf2" frame={frame} />
        </g>
        <g transform="translate(70 58)">
          <PixelWord word={name} px={10} fill={INK} frame={frame} />
        </g>
        <text x={72} y={168} fontFamily={MONO} fontSize={19} fontWeight={700} letterSpacing={3} fill={INK}>
          {subtitle}
        </text>
        <Typing roles={roles} frame={frame} />

        <Sparkle x={720} y={70} frame={frame} delay={0} color="#fffaf2" />
        <Sparkle x={1140} y={110} frame={frame} delay={20} color="#fffaf2" />
        <Sparkle x={1090} y={40} frame={frame} delay={40} color="#2f50a8" />
        <Sparkle x={560} y={60} frame={frame} delay={30} color="#2f50a8" />

        {/* sticker outline like the reference: silhouette in cream, offset around the sprite */}
        {[
          [-1, 0],
          [1, 0],
          [0, -1],
          [1, 1],
          [-1, 1],
        ].map(([dx, dy]) => (
          <g key={`${dx}${dy}`} transform={`translate(${charX + dx * px} ${charY + dy * px})`}>
            <Pixels rows={BASE.map((r) => r.replace(/[^.]/g, 'O'))} px={px} />
          </g>
        ))}
        <g transform={`translate(${charX} ${charY})`}>
          <Osaragi frame={frame} px={px} />
        </g>
        <Nom frame={frame} x={charX + charW - 20} y={charY + 120} />

        <Table />
        <text x={72} y={372} fontFamily="'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', sans-serif" fontSize={22} fontWeight={700} fill="#7a6545">
          {motto}
        </text>
        <text x={W - 24} y={386} textAnchor="end" fontFamily={MONO} fontSize={12} fill="#8f7a58">
          fan-art sprite · Osaragi / Sakamoto Days
        </text>
      </svg>
    </AbsoluteFill>
  );
};
