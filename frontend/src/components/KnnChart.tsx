import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LabelList } from 'recharts';

const ScatterChartComponent = ({ coordinates }) => {
  // Convert the coordinates object into an array of points.
  // Expected input: { "leo": [x, y], "shib": [x, y], "user_score": [x, y] }
  const data = Object.entries(coordinates).map(([name, [x, y]]) => ({ name, x, y }));

  // Custom dot renderer to render white points.
  const renderCustomizedDot = (props) => {
    const { cx, cy } = props;
    return <circle cx={cx} cy={cy} r={5} fill="#ffffff" />;
  };

  return (
    <div className="w-full max-w-md mx-auto bg-white dark:bg-gray-900 p-4 rounded-2xl shadow-lg">
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="x" name="X" type="number" domain={[0, 1]} />
          <YAxis dataKey="y" name="Y" type="number" domain={[0, 1]} />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Scatter name="Coordinates" data={data} dot={renderCustomizedDot}>
            <LabelList dataKey="name" position="top" />
          </Scatter>
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ScatterChartComponent;
