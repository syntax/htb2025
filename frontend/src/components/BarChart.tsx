import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend, Text } from "recharts";

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']; // Custom colors

const BarChartComponent = ({ holdings }) => {
  // Ensure holdings is defined to prevent errors
  const safeHoldings = holdings ?? {}; 

  // Convert object into an array format suitable for Recharts
  const data = Object.entries(safeHoldings).map(([coin, value]) => ({ coin, value }));

  return (
    <div className="w-full max-w-md mx-auto bg-white dark:bg-gray-900 p-4 rounded-2xl shadow-lg">
      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 40, bottom: 40 }}>
          <CartesianGrid strokeDasharray="3 3" />
          
          {/* X-Axis */}
          <XAxis dataKey="coin" stroke="#8884d8">
            <Text x={0} y={0} dx={150} dy={30} fontSize={14} fill="#8884d8">
              Cryptocurrency
            </Text>
          </XAxis>

          {/* Y-Axis */}
          <YAxis tickFormatter={(value) => `$${value}`}>
            <Text x={0} y={0} dx={-30} dy={150} fontSize={14} fill="#8884d8" angle={-90}>
              Price (USD)
            </Text>
          </YAxis>

          <Tooltip formatter={(value) => `$${value}`} />
          <Legend verticalAlign="top" height={30} />
          
          <Bar dataKey="value" fill="#8884d8" barSize={20}>
            {data.map((entry, index) => (
              <rect key={`bar-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BarChartComponent;
