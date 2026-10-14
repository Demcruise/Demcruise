import React from 'react';
import {Composition} from 'remotion';
import {Banner, bannerSchema} from './Banner';

export const Root: React.FC = () => (
  <Composition
    id="Banner"
    component={Banner}
    durationInFrames={240}
    fps={30}
    width={1200}
    height={400}
    schema={bannerSchema}
    defaultProps={{
      name: 'DEMCRUISE',
      subtitle: 'PRODUCT DESIGN · UI/UX · APP UI',
      roles: ['Product Designer', 'UI/UX Designer', 'App UI crafter'],
      motto: '不关我的事 ～',
    }}
  />
);
