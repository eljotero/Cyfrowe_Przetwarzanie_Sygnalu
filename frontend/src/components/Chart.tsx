import { useParams } from 'react-router-dom';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
interface SignalData {
  signalId: number;
  formData: {
    [key: string]: string;
  };
}
function Chart() {
  const { data } = useParams<{ data: string | undefined }>();
  if (!data) {
    return <div>Brak danych</div>;
  }
  let parsedData: SignalData;
  try {
    parsedData = JSON.parse(decodeURIComponent(data));
  } catch (error) {
    return <div>Błąd parsowania danych</div>;
  }
  const generateChartData = (signalId: number) => {
    switch (signalId) {
      case 1: {
        const A = parseInt(parsedData.formData['A']);
        const t1 = parseInt(parsedData.formData['t1']);
        const d = parseInt(parsedData.formData['d']);
        const signalData: number[] = [];
        for (let i = t1; i < d; i++) {
          signalData.push(Math.random() * (2 * A) - A);
        }
        return {
          labels: Array.from({ length: d }, (_, i) => i + t1),
          datasets: [
            {
              data: signalData,
              tension: 0.1,
            },
          ],
        };
      }
      case 2: {
        const A = parseInt(parsedData.formData['A']);
        const t1 = parseInt(parsedData.formData['t1']);
        const d = parseInt(parsedData.formData['d']);
        const signalData: number[] = [];
        for (let i = t1; i < d; i++) {
          signalData.push(
            A *
              Math.pow(
                (1 / 1) * Math.sqrt(2 * Math.PI) * Math.E,
                -Math.pow(Math.random(), 2) / 2
              )
          );
        }
        return {
          labels: Array.from({ length: d }, (_, i) => i + t1),
          datasets: [
            {
              data: signalData,
              tension: 0.1,
            },
          ],
        };
      }
      case 3: {
        const A = parseInt(parsedData.formData['A']);
        const t1 = parseInt(parsedData.formData['t1']);
        const d = parseInt(parsedData.formData['d']);
        const T = parseInt(parsedData.formData['T']);
        const signalData: number[] = [];
        for (let i = t1; i < d; i++) {
          signalData.push(A * Math.sin(((2 * Math.PI) / T) * (i - t1)));
        }
        return {
          labels: Array.from({ length: d }, (_, i) => i + t1),
          datasets: [
            {
              data: signalData,
              tension: 0.1,
            },
          ],
        };
      }
      case 4: {
        const A = parseInt(parsedData.formData['A']);
        const t1 = parseInt(parsedData.formData['t1']);
        const d = parseInt(parsedData.formData['d']);
        const T = parseInt(parsedData.formData['T']);
        const signalData: number[] = [];
        for (let i = t1; i < d; i++) {
          signalData.push(
            (1 / 2) *
              A *
              (Math.sin(((2 * Math.PI) / T) * (i - t1)) +
                Math.abs(Math.sin(((2 * Math.PI) / T) * (i - t1))))
          );
        }
        return {
          labels: Array.from({ length: d }, (_, i) => i + t1),
          datasets: [
            {
              data: signalData,
              tension: 0.1,
            },
          ],
        };
      }
      case 5: {
        const A = parseInt(parsedData.formData['A']);
        const t1 = parseInt(parsedData.formData['t1']);
        const d = parseInt(parsedData.formData['d']);
        const T = parseInt(parsedData.formData['T']);
        const signalData: number[] = [];
        for (let i = t1; i < d; i++) {
          signalData.push(
            A * Math.abs(Math.sin(((2 * Math.PI) / T) * (i - t1)))
          );
        }
        return {
          labels: Array.from({ length: d }, (_, i) => i + t1),
          datasets: [
            {
              data: signalData,
              tension: 0.1,
            },
          ],
        };
      }
      //Ile k?
      case 6: {
        const A = parseInt(parsedData.formData['A']);
        const t1 = parseInt(parsedData.formData['t1']);
        const d = parseInt(parsedData.formData['d']);
        const T = parseInt(parsedData.formData['T']);
        const kw = parseInt(parsedData.formData['kw']);
        const signalData: number[] = [];
        for (let i = t1; i < d; i++) {
          if (i >= 0 * T + t1 && i < kw * T + 0 * T + t1) {
            signalData.push(A);
          } else if (i > kw * T + t1 + 0 * T && i < T + 0 * T + t1) {
            signalData.push(0);
          }
        }
        return {
          labels: Array.from({ length: d }, (_, i) => i + t1),
          datasets: [
            {
              data: signalData,
              tension: 0.1,
            },
          ],
        };
      }
      //Ile k?
      case 7: {
        const A = parseInt(parsedData.formData['A']);
        const t1 = parseInt(parsedData.formData['t1']);
        const d = parseInt(parsedData.formData['d']);
        const T = parseInt(parsedData.formData['T']);
        const kw = parseInt(parsedData.formData['kw']);
        const signalData: number[] = [];
        for (let i = t1; i < d; i++) {
          if (i >= 0 * T + t1 && i < kw * T + 0 * T + t1) {
            signalData.push(A);
          } else if (i > kw * T + t1 + 0 * T && i < T + 0 * T + t1) {
            signalData.push(-A);
          }
        }
        return {
          labels: Array.from({ length: d }, (_, i) => i + t1),
          datasets: [
            {
              data: signalData,
              tension: 0.1,
            },
          ],
        };
      }
      //Ile k?
      case 8: {
        const A = parseInt(parsedData.formData['A']);
        const t1 = parseInt(parsedData.formData['t1']);
        const d = parseInt(parsedData.formData['d']);
        const T = parseInt(parsedData.formData['T']);
        const kw = parseInt(parsedData.formData['kw']);
        const signalData: number[] = [];
        for (let i = t1; i < d; i++) {
          if (i >= 0 * T + t1 && i < kw * T + 0 * T + t1) {
            signalData.push((A / kw) * T);
          } else if (i > kw * T + t1 + 0 * T && i < T + 0 * T + t1) {
            signalData.push((-A / T) * (1 - kw));
          }
        }
        return {
          labels: Array.from({ length: d }, (_, i) => i + t1),
          datasets: [
            {
              data: signalData,
              tension: 0.1,
            },
          ],
        };
      }
      case 9: {
        const A = parseInt(parsedData.formData['A']);
        const t1 = parseInt(parsedData.formData['t1']);
        const d = parseInt(parsedData.formData['d']);
        const ts = parseInt(parsedData.formData['ts']);
        const signalData: number[] = [];
        for (let i = t1; i < d; i++) {
          if (i > ts) {
            signalData.push(A);
          } else if (i === ts) {
            signalData.push((1 / 2) * A);
          } else {
            signalData.push(0);
          }
        }
        return {
          labels: Array.from({ length: d }, (_, i) => i + t1),
          datasets: [
            {
              data: signalData,
              tension: 0.1,
            },
          ],
        };
      }
      case 10: {
        const A = parseInt(parsedData.formData['A']);
        const ns = parseInt(parsedData.formData['ns']);
        const n1 = parseInt(parsedData.formData['n1']);
        const l = parseInt(parsedData.formData['l']);
        const f = parseInt(parsedData.formData['f']);
        const signalData: number[] = [];
        for (let i = n1; i < n1 + l; i++) {
          if (i === ns) {
            signalData.push(1);
          } else {
            signalData.push(0);
          }
        }
        return {
          labels: Array.from({ length: l }, (_, i) => i + n1),
          datasets: [
            {
              data: signalData,
              tension: 0.1,
            },
          ],
        };
      }
      case 11: {
        const A = parseInt(parsedData.formData['A']);
        const t1 = parseInt(parsedData.formData['t1']);
        const d = parseInt(parsedData.formData['d']);
        const f = parseInt(parsedData.formData['f']);
        const p = parseInt(parsedData.formData['p']) / 100;
        const signalData: number[] = [];
        for (let i = t1; i < d; i++) {
          const rand = Math.random();
          if (rand > p) {
            signalData.push(0);
          } else {
            signalData.push(A);
          }
        }
        return {
          labels: Array.from({ length: d }, (_, i) => i + t1),
          datasets: [
            {
              data: signalData,
              tension: 0.1,
            },
          ],
        };
      }

      default:
        return null;
    }
  };
  const chartData = generateChartData(parsedData.signalId);

  if (!chartData) {
    return (
      <div>Nie znaleziono danych dla sygnału o id {parsedData.signalId}</div>
    );
  }

  var options = {
    maintainAspectRatio: false,
    responsive: true,
  };

  return (
    <div className='chartcontainer'>
      <Line data={chartData} options={options} />
    </div>
  );
}

export default Chart;
