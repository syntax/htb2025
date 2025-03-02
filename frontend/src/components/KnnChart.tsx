import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LabelList } from 'recharts';

const ScatterChartComponent = ({ coordinates }) => {
  const data = Object.entries(coordinates).map(([name, [x, y]]) => ({ name, x, y }));

  const renderCustomizedDot = (props) => {
    const { cx, cy } = props;
    return (
      <circle 
        cx={cx} 
        cy={cy} 
        r={6}
        fill="#fff" 
        stroke="#rgba(0, 0, 0, 0.3)"
        strokeWidth={1.5}
        className="z-10" 
      />
    );
  };

  return (
    <div className="w-full max-w-md mx-auto bg-white dark:bg-gray-900 p-4 rounded-2xl shadow-lg">
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart
          margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
          style={{ background: 'inherit' }}  // Inherit parent's background
        >
          <CartesianGrid 
            strokeDasharray="3 3" 
            stroke="#64748b"  // Slate-500 for better visibility
          />
          <XAxis 
            dataKey="x" 
            type="number" 
            domain={[0, 1]} 
            tick={{ fill: '#94a3b8' }}  // Slate-400
            axisLine={{ stroke: '#94a3b8' }}
          />
          <YAxis 
            dataKey="y" 
            type="number" 
            domain={[0, 1]} 
            tick={{ fill: '#94a3b8' }}  // Slate-400
            axisLine={{ stroke: '#94a3b8' }}
          />
          <Tooltip 
            cursor={{ strokeDasharray: '3 3' }}
            contentStyle={{
              background: '#1e293b',  // Slate-800
              border: 'none',
              borderRadius: '8px',
              color: '#fff'
            }}
          />
          <Scatter 
            name="Coordinates" 
            data={data} 
            fill="#fff"
            dot={renderCustomizedDot}
          >
            <LabelList 
              dataKey="name" 
              position="top" 
              fill="#fff"
              style={{ fontSize: '12px', fontWeight: 500 }}
            />
          </Scatter>
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ScatterChartComponent;